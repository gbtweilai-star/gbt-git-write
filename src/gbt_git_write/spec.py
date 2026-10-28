"""The capability contract, copied verbatim from the GBT V8 registry.

Do not hand-edit: ``tests/test_spec.py`` pins every field against the
registry snapshot so drift fails the build instead of shipping quietly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

_RAW = r"""{
 "name": "git_write",
 "domain": "tools",
 "desc": "**版本库写面**（只两个 op，且**永远要点名路径**）：stage（`git add -- <paths>`）· commit（**pathspec-limited**：`git commit -m … -- <paths>`，只提交点名的路径，**不动索引里别的暂存内容**）。为什么必须点名：本仓脏行可能上万，`commit -a` 一次就把不相干的全卷进去。**永远挂 `filesystem_write`**（不按 op 判 —— 拆成独立能力位就是为了让门的判据平凡正确）。与 `git_read` 分开登记：`safe` 是按能力位记的，不是按 op 记的。type=internal",
 "handler": "git_write",
 "safe": false,
 "external": false,
 "requires_params": true,
 "params": [
  "paths",
  "message"
 ],
 "params_hint": "paths=要动的仓内路径列表（**必填、不许空**）；commit 还要 message；op=stage|commit",
 "multi_op": true,
 "ops": [],
 "ops_hint": "paths=要动的仓内路径列表（**必填、不许空**）；commit 还要 message；op=stage|commit"
}"""


@dataclass(frozen=True)
class CapSpec:
    """Immutable description of one capability bit."""

    name: str
    domain: str
    desc: str
    handler: str
    safe: bool
    external: bool
    requires_params: bool
    params: Tuple[str, ...] = ()
    params_hint: str = ""
    multi_op: bool = False
    ops: Tuple[str, ...] = ()
    ops_hint: str = ""

    @property
    def gated(self) -> bool:
        """True when the registry marks this bit ``safe: false``.

        Gated does not mean "dangerous"; it means the action can change state
        that cannot be restored by running the inverse action.
        """
        return not self.safe

    @property
    def summary(self) -> str:
        """First clause of the description, for one-line listings."""
        for sep in ("\uff08", "\uff1b", "\u3002", ";"):
            if sep in self.desc:
                head = self.desc.split(sep, 1)[0].strip()
                if head:
                    return head
        return self.desc.strip()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "desc": self.desc,
            "handler": self.handler,
            "safe": self.safe,
            "gated": self.gated,
            "external": self.external,
            "requires_params": self.requires_params,
            "params": list(self.params),
            "params_hint": self.params_hint,
            "multi_op": self.multi_op,
            "ops": list(self.ops),
            "ops_hint": self.ops_hint,
        }


_data = json.loads(_RAW)

SPEC = CapSpec(
    name=_data["name"],
    domain=_data["domain"],
    desc=_data["desc"],
    handler=_data["handler"],
    safe=_data["safe"],
    external=_data["external"],
    requires_params=_data["requires_params"],
    params=tuple(_data["params"]),
    params_hint=_data["params_hint"],
    multi_op=_data["multi_op"],
    ops=tuple(_data["ops"]),
    ops_hint=_data["ops_hint"],
)
