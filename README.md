# 星雀 `xingque`

Yet another Python binding to [`starlark-rs`][starlark-rs], exposing the
[Starlark] language to your Python projects. The current version wraps
`starlark-rs` version 0.12.x.

The project's name is a [calque] of "Starlark" into Chinese. It is
pronounced *xīng què* (in Standard Pinyin) or *Hsing-ch'üeh* (in Wade-Giles).

<details>
<summary>The reason behind the curious name</summary>

I had to come up with another name for the project after discovering
[an identically named project][starlark-pyo3] after I first renamed the
project `starlark-pyo3` from `python-starlark-rs`, and that the probably
next-best alternative `pystarlark` was also taken long ago.

</details>

[calque]: https://en.wikipedia.org/wiki/Calque
[starlark-pyo3]: https://github.com/inducer/starlark-pyo3
[starlark-rs]: https://github.com/facebook/starlark-rust
[Starlark]: https://github.com/bazelbuild/starlark

**NOTE: this project is still under development, do not use in production yet.**

## Work in Progress

* [ ] `starlark::analysis`
* [ ] `starlark::any`
* [ ] `starlark::assert`
* [x] `starlark::codemap` -- majority completed
    - [x] `CodeMap`
    - [ ] `CodeMapId`
    - [x] `FileSpan`
    - [ ] `FileSpanRef`
    - [ ] `NativeCodeMap`
    - [x] `Pos`
    - [x] `ResolvedFileLine`
    - [x] `ResolvedFileSpan`
    - [x] `ResolvedPos`
    - [x] `ResolvedSpan`
    - [x] `Span`
    - [ ] `Spanned`
* [ ] `starlark::coerce`
* [ ] `starlark::collections`
* [ ] `starlark::debug`
* [ ] `starlark::docs`
* [ ] `starlark::environment`
    - [ ] `FrozenModule`
    - [x] `Globals` -- mostly done
    - [x] `GlobalsBuilder` -- mostly done
    - [ ] `GlobalsStatic`
    - [ ] `Methods`
    - [ ] `MethodsBuilder`
    - [ ] `MethodsStatic`
    - [ ] `Module`
    - [x] `LibraryExtension`
* [ ] `starlark::errors`
* [ ] `starlark::eval`
* [x] `starlark::syntax`
    - [x] `DialectTypes`
    - [x] `Dialect`
    - [x] `AstLoad`
    - [x] `AstModule`
* [ ] `starlark::typing`
* [ ] `starlark::values`
    - [ ] `AggregateHeapProfileInfo`
    - [ ] `Demand`
    - [ ] `Freezer`
    - [ ] `FrozenHeap`
    - [ ] `FrozenHeapRef`
    - [ ] `FrozenRef`
    - [ ] `FrozenValue`
    - [ ] `FrozenValueTyped`
    - [x] `Heap` -- partially done
    - [ ] `OwnedFrozenRef`
    - [ ] `OwnedFrozenValue`
    - [ ] `OwnedFrozenValueTyped`
    - [ ] `StarlarkIterator`
    - [ ] `StarlarkStrNRepr`
    - [ ] `Tracer`
    - [ ] `Value`
    - [ ] `ValueIdentity`
    - [ ] `ValueOf`
    - [ ] `ValueOfUnchecked`
    - [ ] `ValueTyped`
    - [ ] `ValueTypedComplex`

## License

Copyright &copy; 2024 WANG Xuerui. All rights reserved.

`xingque` is licensed under either the
[Apache 2.0 license](./LICENSE.Apache-2.0) or the
[MIT license](./LICENSE.MIT).
