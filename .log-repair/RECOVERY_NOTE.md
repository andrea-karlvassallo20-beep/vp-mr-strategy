# Log recovery note

The log-recovery workflow ran on PR open and completed on 2026-11-20: payloads decoded
against manifest sha256s, programme log restored (entries ## 1-73 verbatim from parent
blob 8fad9367, ## 74 from the PR #250 squash message, ## 75 corrigendum, ## 76 edition-4
synthesis pass, ## 77 deep-read 60), payloads git rm'd. This file re-triggers CI because
GITHUB_TOKEN pushes from the bot do not trigger workflow runs.

Guard clean. Nothing measured, no kill line moved, nothing armed, nothing trades live.
