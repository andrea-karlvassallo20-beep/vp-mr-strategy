# Log restore note 72

The log_restore_72b workflow ran on PR synchronize and completed on
2026-11-20: payloads decoded against the manifest sha256
(3f7251c220939ce5f81c9c4379d73607adb4bb8cb911dc68e2accb8075f3286f),
programme log restored to 481148 bytes (entries ## 78 and ## 79 landed),
payloads and scaffold removed. The first run (72) decoded correctly but
committed only the payload removals (unstaged restore); 72b stages the
target explicitly. GITHUB_TOKEN pushes do not trigger workflow runs; this
commit re-triggers CI for the final head.

Guard clean. Nothing measured, no kill line moved, nothing armed, nothing trades live.
