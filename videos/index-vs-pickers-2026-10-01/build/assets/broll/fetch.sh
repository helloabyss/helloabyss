#!/usr/bin/env bash
# B-roll stills for "93% of Pros" — Higgsfield gpt_image_2_5, 9:16, 752x1344, generated 2026-10-01 (2.5 credits total).
# Needs network access to d8j0ntlcm91z4.cloudfront.net (Higgsfield's file host).
set -euo pipefail
cd "$(dirname "$0")"
B=https://d8j0ntlcm91z4.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM
while read -r name file; do
  [ -s "$name" ] || curl -fsS -m 60 -o "$name" "$B/$file"
done <<'LIST'
b00-trading-floor.png hf_20261001_061640_ae02477e-e517-4930-b932-4fb3bd4ea396.png
b01-tower-up.png hf_20261001_061724_183dd234-b06d-4e80-976a-1b737cad80d2.png
b02-screen-wall.png hf_20261001_061724_642cbf60-48f2-4bf4-925a-7dc7d3d83902.png
b03-lobby.png hf_20261001_061725_802cc3c5-494d-4181-88e1-2dbaa1731c37.png
b04-trophy.png hf_20261001_061744_51b13a33-92b1-4ef9-9a8f-b368623fdb9c.png
b05-boardroom.png hf_20261001_061724_8f4c8d3e-d940-49b1-a7c8-bad96af00229.png
b06-dawn-skyline.png hf_20261001_061725_ede025ae-de46-45bb-9849-ab71ec244e33.png
b07-storm.png hf_20261001_061724_2874916d-65b6-4c19-94a8-5aaea876d158.png
b08-coins.png hf_20261001_061724_afab6bcc-b68e-43c7-a70e-4b1c38033769.png
b09-laptop.png hf_20261001_061724_7ba76a88-4aad-4490-8128-c33e838be755.png
LIST
ls -la
