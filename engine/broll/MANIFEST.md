# B-roll plates — source and licence

The plate files themselves are **not committed**. Adobe Stock licences cover using an
asset *in a work*; committing the asset (or a lightly graded derivative of it) to a
repository is redistribution, and this repository may be public. Only this manifest is
tracked, so the set can be re-fetched.

All five are **Adobe Stock free collection**, licensed to the channel's Adobe account on
2026-10-08 at **no cost** (`"pricing":"free"`, `state: just_purchased`).

| File | Adobe Stock ID | Subject | Native | Used on beats |
|---|---|---|---|---|
| `dish-array.jpg` | `425564576` | Satellite dish silhouettes against a night sky | 6720×4480 | 0, 14, 15 |
| `datacentre.jpg` | `180573482` | Data centre interior | 7360×4365 | 22, 25 |
| `substation.jpg` | `449898303` | Electric substation at dusk | 7360×4912 | 24 |
| `wafer.jpg` | `477534477` | Surface of silicon wafers and microcircuits | 7381×4377 | 28, 31 |
| `racks.jpg` | `286399132` | Data centre storage racks | 7000×3789 | 37 |

## Re-fetching

`asset_search` with `entityScope: "StockAsset"` → `asset_license_and_download_stock` with
the ID above → download the returned presigned URL to `engine/broll/<file>.jpg`. Then:

```
node prep_broll.js        # grades + downscales to <file>-graded.jpg, which the build reads
```

## Why these and not generated plates

- **Higgsfield is unusable as a b-roll source from this environment.** Three good plates
  already exist in the account (a rocket launch and two data-centre montages) and cannot
  be retrieved: the CDN `d8j0ntlcm91z4.cloudfront.net` returns **403 on CONNECT** at the
  agent proxy, a policy denial that no retry fixes. Generating more there spends credits
  on files that cannot be downloaded. **Do not.**
- **ElevenLabs creative generation is unavailable through the MCP bridge**, which returns
  a schema-validation error for `creative_generate_image`, `creative_attach_reference_file`,
  `creative_get_model_guide` and `creative_get_available_assets`. `creative_list_voices`
  and `creative_get_flow` work, so the bridge itself is up — the failure is tool-specific.
  A failed call may still have spent server-side, so do not retry these blindly.

## Editorial rules applied

Every plate is a **real photograph** of the *category* — satellite communications, data
centres, grid power, silicon. None depicts SpaceX, Bloom Energy or Micron, and none is
captioned as though it does. No logos, no identifiable people. Graded to near-monochrome
so the only colour in frame is the red accent, per `STYLE-GUIDE.md`.
