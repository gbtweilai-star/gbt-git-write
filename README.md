# git_write

**One capability bit from GBT V8, packaged standalone.** No. 315 of 341,
`tools` domain (Tools).

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
</p>

> **版本库写面**（只两个 op，且**永远要点名路径**）：stage（`git add -- <paths>`）· commit（**pathspec-limited**：`git commit -m … -- <paths>`，只提交点名的路径，**不动索引里别的暂存内容**）。为什么必须点名：本仓脏行可能上万，`commit -a` 一次就把不相干的全卷进去。**永远挂 `filesystem_write`**（不按 op 判 —— 拆成独立能力位就是为了让门的判据平凡正确）。与 `git_read` 分开登记：`safe` 是按能力位记的，不是按 op 记的。type=internal

That description is copied verbatim from the registry. `tests/test_spec.py` pins it,
so documentation drift fails the build instead of shipping quietly.

## What this package actually is

It is the **contract** for one capability: its name, its parameters, the values it
accepts, and whether it can change state that cannot be restored. It is not the
implementation — that lives in the runtime this bit was extracted from.

So `run()` goes through a narrow `Backend` protocol, and the default backend is a
stub that **says so**:

```
status="validated"   backend="stub"   data={"executed": false}
```

Never `status="ok"`. A stub that reports success is worse than no stub, because the
caller stops looking for the real thing.

## Install

```bash
git clone https://github.com/gbtweilai-star/gbt-git-write.git
cd gbt-git-write
python -m pip install -e ".[dev]"
```

## Use

```bash
python -m gbt_git_write info                  # capability card
python -m gbt_git_write spec --json           # machine-readable contract
python -m gbt_git_write check --payload '{"paths": "<在此填写>", "message": "<在此填写>"}'
python -m gbt_git_write run   --payload '{"paths": "<在此填写>", "message": "<在此填写>"}'
```

Real `info` output from this machine:

```text
git_write  (tools)  v1.0.0
----------------------------------------
**版本库写面**（只两个 op，且**永远要点名路径**）：stage（`git add -- <paths>`）· commit（**pathspec-limited**：`git commit -m … -- <paths>`，只提交点名的路径，**不动索引里别的暂存内容**）。为什么必须点名：本仓脏行可能上万，`commit -a` 一次就把不相干的全卷进去。**永远挂 `filesystem_write`**（不按 op 判 —— 拆成独立能力位就是为了让门的判据平凡正确）。与 `git_read` 分开登记：`safe` 是按能力位记的，不是按 op 记的。type=internal

gated      : True   <- needs explicit consent
external   : False
multi-op   : True
params     : paths, message
             paths=要动的仓内路径列表（**必填、不许空**）；commit 还要 message；op=stage|commit
values     : (multi-op, but the registry does not enumerate them)
```

Wire a real implementation:

```python
from gbt_git_write import run

class MyBackend:
    name = "my-backend"
    def invoke(self, cap, payload):
        return {"cap": cap, "handled": sorted(payload)}

result = run({"paths": "<在此填写>", "message": "<在此填写>"}, backend=MyBackend())
assert result.status == "ok"
```

## Parameters

| name | required | notes |
|---|---|---|
| `paths` | yes | declared required by the registry |
| `message` | yes | declared required by the registry |

Registry hint (`params_hint`): paths=要动的仓内路径列表（**必填、不许空**）；commit 还要 message；op=stage|commit

**注册表标注 `multi_op: true`，但没有枚举具体取值。**本包不替它编造取值清单——这种缺口应当在注册表源头补，而不是在文档里圆。

Types are deliberately absent: the registry does not declare them, and an invented
type is worse than no type, because callers believe it.

## Boundaries

- Gated: this bit is marked `safe: false` in the registry — it can change state that no inverse action restores.
- No external service dependency declared.
- Multi-op (`multi_op: true`): several sub-actions share one name — read `op` before calling.
- No implementation ships here. Bring a backend; the protocol is one method.

## What this is not

Not a wrapper around a hosted API. Not a model. Not a promise that calling it does
anything on its own. It is the typed seam plus the validation, which is the part that
stays correct even when the implementation changes.

## Tests

```bash
python -m pytest
```

```text
23 passed, 1 skipped in 0.11s
```

## Provenance

| field | value |
|---|---|
| capability | `git_write` |
| domain | `tools` |
| handler | `git_write` |
| safe | `False` (gated = `True`) |
| external | `False` |
| atlas page | [tools/git_write](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/tools/git_write.md) |
| full index | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

The parent README says 348 capabilities; an AST pass over the registry enumerates
`341 + 0 unimplemented + 0 disabled = 341`. The extra 7 are historical duplicates.
Numbering here follows 341 and matches the `gbt-caps` index one-to-one.

## License

MIT.
