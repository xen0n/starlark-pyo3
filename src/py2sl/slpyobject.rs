use core::cmp::Ordering;
use std::hash::Hasher;

use allocative::Allocative;
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::types::PyTuple;
use starlark::any::ProvidesStaticType;
use starlark::collections::StarlarkHasher;
use starlark::eval::{Arguments, Evaluator};
use starlark::values::{
    starlark_value, AllocFrozenValue, AllocValue, Freeze, Freezer, FrozenHeap, FrozenValue, Heap,
    NoSerialize, StarlarkValue, Trace, Value,
};

use crate::py2sl::sl_value_from_py;
use crate::sl2py::py_from_sl_value;

#[derive(Trace, NoSerialize, ProvidesStaticType, Allocative)]
pub(crate) struct SlPyObject(#[allocative(skip)] pub(crate) PyObject);

impl From<PyObject> for SlPyObject {
    fn from(value: PyObject) -> Self {
        Self(value)
    }
}

impl<'v> AllocValue<'v> for SlPyObject {
    fn alloc_value(self, heap: &'v Heap) -> Value<'v> {
        heap.alloc_simple(self)
    }
}

impl AllocFrozenValue for SlPyObject {
    fn alloc_frozen_value(self, heap: &FrozenHeap) -> FrozenValue {
        heap.alloc_simple(self)
    }
}

impl ::core::fmt::Debug for SlPyObject {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        ::core::fmt::Debug::fmt(&self.0, f)
    }
}

impl ::std::fmt::Display for SlPyObject {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        ::std::fmt::Display::fmt(&self.0, f)
    }
}

impl Freeze for SlPyObject {
    type Frozen = SlPyObject;

    fn freeze(self, _freezer: &Freezer) -> anyhow::Result<Self::Frozen> {
        Ok(self)
    }
}

#[starlark_value(type = "pyobject")]
impl<'v> StarlarkValue<'v> for SlPyObject {
    type Canonical = Self;

    fn to_bool(&self) -> bool {
        let result: PyResult<bool> = Python::with_gil(|py| {
            let inner = self.0.bind(py);
            inner.is_truthy()
        });
        result.unwrap_or(true)
    }

    fn write_hash(&self, hasher: &mut StarlarkHasher) -> starlark::Result<()> {
        Python::with_gil(|py| {
            let inner = self.0.bind(py);
            match inner.hash() {
                Ok(hash) => {
                    hasher.write_isize(hash);
                    Ok(())
                }
                Err(e) => Err(starlark::Error::new(starlark::ErrorKind::Value(e.into()))),
            }
        })
    }

    fn equals(&self, other: Value<'v>) -> starlark::Result<bool> {
        let result: PyResult<bool> = Python::with_gil(|py| {
            let inner = self.0.bind(py);
            let other = py_from_sl_value(py, other)?;
            inner.eq(other)
        });

        result.map_err(|e| starlark::Error::new(starlark::ErrorKind::Value(e.into())))
    }

    fn compare(&self, other: Value<'v>) -> starlark::Result<Ordering> {
        let result: PyResult<Ordering> = Python::with_gil(|py| {
            let inner = self.0.bind(py);
            let other = py_from_sl_value(py, other)?;
            inner.compare(other)
        });

        result.map_err(|e| starlark::Error::new(starlark::ErrorKind::Value(e.into())))
    }

    fn invoke(
        &self,
        _me: Value<'v>,
        args: &Arguments<'v, '_>,
        eval: &mut Evaluator<'v, '_>,
    ) -> starlark::Result<Value<'v>> {
        let heap = eval.heap();
        let result: PyResult<Value<'v>> = Python::with_gil(|py| {
            let inner = self.0.bind(py);

            let py_args = {
                let mut result = Vec::new();
                match args.positions(heap) {
                    Ok(sl_args) => {
                        for sl in sl_args {
                            result.push(py_from_sl_value(py, sl)?);
                        }
                    }
                    Err(e) => {
                        return Err(PyRuntimeError::new_err(format!(
                            "failed to unpack Starlark positional args: {}",
                            e.to_string()
                        )));
                    }
                }
                PyTuple::new_bound(py, result)
            };

            let py_kwargs = match args.names_map() {
                Ok(sl_kwargs) => {
                    if sl_kwargs.len() == 0 {
                        None
                    } else {
                        let result = PyDict::new_bound(py);
                        for (k, v) in sl_kwargs {
                            let k = k.as_str();
                            match py_from_sl_value(py, v) {
                                Ok(v) => {
                                    if let Err(e) = result.set_item(k, v) {
                                        return Err(e);
                                    }
                                }
                                Err(e) => {
                                    return Err(e);
                                }
                            }
                        }
                        Some(result)
                    }
                }

                Err(e) => {
                    return Err(PyRuntimeError::new_err(format!(
                        "failed to unpack Starlark keyword args: {}",
                        e.to_string()
                    )));
                }
            };

            inner
                .call(py_args, py_kwargs.as_ref())
                .map(|v| sl_value_from_py(&v, heap))
        });

        result.map_err(|e| starlark::Error::new(starlark::ErrorKind::Value(e.into())))
    }

    fn length(&self) -> starlark::Result<i32> {
        Python::with_gil(|py| {
            let inner = self.0.bind(py);
            match inner.len() {
                Ok(len) => Ok(len as i32),
                Err(e) => Err(starlark::Error::new(starlark::ErrorKind::Value(e.into()))),
            }
        })
    }

    fn is_in(&self, other: Value<'v>) -> starlark::Result<bool> {
        let result = Python::with_gil(|py| {
            let inner = self.0.bind(py);
            let other = py_from_sl_value(py, other)?;
            inner.contains(other)
        });

        result.map_err(|e| starlark::Error::new(starlark::ErrorKind::Value(e.into())))
    }

    // TODO: plus/minus only wrappable after
    // https://github.com/PyO3/pyo3/commit/37a5f6a94e9dab31575b016a4295fb94322b9aba
    // gets shipped in a published tag
    /*
    fn plus(&self, heap: &'v Heap) -> starlark::Result<Value<'v>> {
        let result = Python::with_gil(|py| {
            let inner = self.0.bind(py);
            inner.pos()
        });

        result.map_err(|e| starlark::Error::new(starlark::ErrorKind::Value(e.into())))
    }
    */

    fn get_attr(&self, attribute: &str, heap: &'v Heap) -> Option<Value<'v>> {
        Python::with_gil(|py| {
            let inner = self.0.bind(py);
            // no way to propagate error with this interface
            if let Some(v) = inner.getattr(attribute).ok() {
                Some(sl_value_from_py(&v, heap))
            } else {
                None
            }
        })
    }

    fn has_attr(&self, attribute: &str, _heap: &'v Heap) -> bool {
        Python::with_gil(|py| {
            let inner = self.0.bind(py);
            // no way to propagate error with this interface
            inner.hasattr(attribute)
        })
        .unwrap_or(false)
    }

    fn dir_attr(&self) -> Vec<String> {
        Python::with_gil(|py| {
            let inner = self.0.bind(py);
            inner
                .dir()
                .into_iter()
                .map(|x| x.extract::<String>().unwrap())
                .collect()
        })
    }

    fn set_attr(&self, attribute: &str, new_value: Value<'v>) -> starlark::Result<()> {
        Python::with_gil(|py| {
            let inner = self.0.bind(py);
            let new_value = py_from_sl_value(py, new_value)?;
            inner.setattr(attribute, new_value)
        })
        .map_err(|e| starlark::Error::new(starlark::ErrorKind::Value(e.into())))
    }
}
