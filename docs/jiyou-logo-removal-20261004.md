# JIYOU 로고 제거 — 2026-10-04

상태: **원본 덮어쓰기 완료**. 2026-10-04 사용자 승인에 따라 손실 재압축으로 마스크 밖 픽셀이 미세하게 달라지는 것은 허용하며, 저장 전 마스크 밖 차이 0을 기준으로 검증했습니다. 50개 파일을 원래 경로·파일명으로 덮어썼습니다. 아래 수정 후 SHA-256은 실제 덮어쓴 파일 기준이며 보정본과의 바이트 일치를 확인했습니다.

## 처리 및 검수

- 각 사진의 가장 큰 WebP를 먼저 보정한 뒤 Lanczos로 축소했습니다. 축소된 결과의 마스크 영역만 각 크기·형식 원본 위에 합성했습니다. 동일 사진의 AVIF에도 같은 보정을 적용했습니다.
- 모션 이미지 5개는 원본 색감·구도·알파가 다르므로 각각 직접 보정했습니다.
- 마스크는 스티커/로고 및 사용자가 추가 보정을 요청한 돔 인접 경계에 한정하며 보통 1~2 px Gaussian feather를 적용했습니다. 카메라에 가려진 스티커는 전경 경계 추적으로 카메라를 보호했습니다.
- 50개 모두 저장 전 마스크 밖 RGB 차이 0 픽셀. 저장 후에는 손실 압축에 의한 차이가 있으며 RGB 채널 평균 절대 오차는 파일별 0.079~2.523 / 255입니다. 사용자가 허용한 재압축 차이이며, 저장 전 마스크 밖 차이 0 기준을 충족합니다.
- 50개 모두 원래 가로·세로 픽셀 및 형식 일치. 알파 채널이 있는 파일은 저장 후에도 원래 알파와 완전 동일한지 검사했습니다.
- 50개 최종 보정본을 다시 디코딩하여 해당 영역을 확대 검수했습니다. JIYOU / JIYOUENG / 초록 소용돌이와 스티커 인쇄 잔여는 확인되지 않았습니다. OCR 대신 직접 확대 검수를 사용했습니다.
- 파일별 용량 변화: -19.70%~+12.00%, 모두 ±20% 이내. 합계 2,938,272 → 3,142,344 bytes (+6.95%).
- HTML, CSS, JavaScript, 데이터 파일은 변경하지 않았고 commit/push/branch 조작도 하지 않았습니다. 기존 `output/` 내용은 유지했습니다. 모든 작업 파일은 이 worktree 안에 있습니다.

## 돔 경계 추가 보정 및 최종 확인

- 추가 보정 범위: `hook` 3개 WebP, `collision_scene` 12개 WebP/AVIF, `motion_hook` 1개 WebP, 합계 16개. 나머지 34개 보정본은 이전 검수본과 SHA-256이 동일합니다.
- 원본 돔의 아래쪽 곡선을 기준으로 얇은 경계 띠만 다시 합성했습니다. 강건 곡선 근사, 약 1.7 px 안티에일리어싱, 바로 아래 함체 표면의 옅은 접촉 그림자를 적용해 흰 점과 톱니를 정리했습니다. 돔 전체의 이동·크기 변경은 하지 않았습니다.
- 3개 중간 마스터와 최종 압축 출력 16개 모두 100% 및 300% 확대에서 직접 확인했습니다. 검수판은 `.jiyou-work/*-edge-review-100.png`, `*-edge-review-300.png`, `final-edge-qa-1.png` ~ `final-edge-qa-4.png`입니다.
- 덮어쓰기 후 50개 실제 파일의 SHA-256, 픽셀 크기, 형식, 용량, 알파 채널 및 저장 전 마스크 밖 픽셀 보존을 재검증했습니다. Git 추적 파일 변경 목록은 지정한 이미지 50개와 정확히 일치합니다.
- `.jiyou-work/`는 작업 기록으로 그대로 보관하며 커밋 대상에 추가하지 않았습니다. 수정 전 원본 백업도 이 폴더에 있습니다.

## 원본 마스터 조사

저장소 안 원본 없음. `git ls-files`로 확인한 이미지 3,038개의 목록, 별도 source/original/master 경로, 대상 관련 scripts 및 data 참조를 조사했습니다. 파생 이미지·모션 파일을 제외한 너비 950 px 이상 파일은 축소 RGB 유사도 비교도 했으며 같은 사진의 고해상 원본 후보를 찾지 못했습니다. `scripts/product_editorial.py`는 `data/product-editorial-images.json`을 읽고 해당 `media/derived/` 파일을 직접 참조합니다. 이번 편집을 위해 만든 `.jiyou-work/originals/`는 작업 전 백업이며 기존 저장소 마스터가 아닙니다.

## 묶음별 방법 및 가장 큰 파일 SHA-256

각 크기별 원본 파일명 전체는 다음 절에 기재합니다.

| 가장 큰 원본 파일 | 지운 내용 | 방법 | 수정 전 SHA-256 | 수정 후 SHA-256 | 별도 원본 |
|---|---|---|---|---|---|
| `media/derived/product-hook-bottom-camera-reference-white-20260912-1254.webp` | 함체 스티커 전체; 카메라 돔 및 MODY EYE 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 + 돔 경계 추적·조화함수 경계 보정 + 하단 곡선 안티에일리어싱·접촉 그림자 | `b4013ad4fdb9151832f194ba8632133baac6fea9ed08a7db5b33c7447f4efb6d` | `249a6d5e66952748f3606af035bb418279509d35d53381f7dfd9fb2942eec7ed` | 저장소 안 원본 없음 |
| `media/derived/product-tower-crane-hook-collision-reference-white-20260912-1080.webp` | 함체 스티커 전체 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 | `ce634a1be74c954a9122d57697df050c1c6779f71c0ecedcbbb1c6d930159842` | `44b28c2edecbb698da938be0fb4cfb5aa42a5e563a0fbfbf9393029de580b23c` | 저장소 안 원본 없음 |
| `media/derived/product-lte-anemometer-white-approved-20260912-1002.webp` | 함체 스티커 전체 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 | `7b36b4df5a297732571a486db37049f02551c2007be6d1a59eeb35ad47c137ad` | `e83ace02c3c5235f2c3e85c8366eb4c45e5aad1ac41cb0e09f86df9a0648ed80` | 저장소 안 원본 없음 |
| `media/derived/product-iot-small-tower-crane-reference-white-20260912-1280.webp` | 검은 판 왼쪽 초록 소용돌이와 JIYOU 인쇄; 바람개비·후크·숫자·한글 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 | `ee1aabb43d0ec387425f809d73b7aa55a6eb8a9d1134746fd4d44d0e0226bd46` | `8363d1107a2fa3bcf7ca75fc01aad19fabf15dead9b9202dc30d72b566c9e774` | 저장소 안 원본 없음 |
| `media/derived/product-smart-environment-board-reference-white-20260912-1280.webp` | 파란 판 오른쪽 위 흰 소용돌이와 JIYOU | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 | `83e904970ba5a0c5852b5c4b5cd8d556a277352bba7b028fdd5e2bc7bc789b59` | `c4c039a7ec5c34f2f147256445a6ef874893eda1d3e8276b30cb37eadcea17f3` | 저장소 안 원본 없음 |
| `media/derived/product-smart-environment-board-device-1280.avif` | 옥상 전광판 오른쪽 위 로고, 기둥 함체 상단 스티커 및 하단 로고 라벨 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 | `76a9a3e8ca93b2cb9fa572a5d188da65526e676eeb8a07eea0e9e2272369de2c` | `c7c564c0b170493e05469b7547a7249c2832379236d223654cf8f483ccfa2248` | 저장소 안 원본 없음 |
| `media/derived/product-smart-environment-board-device-1280.webp` | 옥상 전광판 오른쪽 위 로고, 기둥 함체 상단 스티커 및 하단 로고 라벨 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 | `93767edc136a6f93143dacb250c37eada794fe44207775c67d45a749b29a16c5` | `a0f605ec7ed74fabd5cb87b8bc594f8d9d97726956b4c74393a07f3cdc6b5642` | 저장소 안 원본 없음 |
| `media/derived/product-smart-environment-board-scene-2560.avif` | 함체 3개 스티커 전체; 진동·소음·미세먼지 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 | `2e914e2b6840fd0052753fbad512578e1fbba63deec4d25c5172e4448919ef37` | `f5cb55344f08e5816719ee14aae9285a3b8bd60eb377ac1f0c6474aad5baae13` | 저장소 안 원본 없음 |
| `media/derived/product-smart-environment-board-scene-2560.webp` | 함체 3개 스티커 전체; 진동·소음·미세먼지 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 | `f655580722e0c58f7adc060a72e2dedae783640d712bee9ba49390d563a04cbb` | `9a5a0f9e357a6dc0caa573c4df5069ebab1c5e1f9d381a0141f23354d88f80ac` | 저장소 안 원본 없음 |
| `media/derived/product-tower-crane-hook-collision-scene-2560.avif` | 줄무늬 기둥 함체 스티커 전체; 카메라 돔 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 + 돔 경계 추적·조화함수 경계 보정 + 하단 곡선 안티에일리어싱·접촉 그림자 | `56ff96d0b58b162b5b39b7085ae0fc3febbf213edcef2158aa21b251998f15cf` | `8446531379788cd7d78429994fa1335782d4897c1d8880007f757be7eb20b2ae` | 저장소 안 원본 없음 |
| `media/derived/product-tower-crane-hook-collision-scene-2560.webp` | 줄무늬 기둥 함체 스티커 전체; 카메라 돔 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 + 돔 경계 추적·조화함수 경계 보정 + 하단 곡선 안티에일리어싱·접촉 그림자 | `c5de2b8f8d8a69eb7e3d576e3de483ee3d0434c1b67e8c81bc43957af1923012` | `f0e7263fc875f7ce2fc0e1d4cd8f26d11a5819cd4bea1df26e86563d60fb0dc1` | 저장소 안 원본 없음 |
| `assets/motion-expanded/hook-bottom-camera-480.webp` | 함체 스티커 전체; MODY EYE·돔·알파 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 + 돔 경계 추적·조화함수 경계 보정 + 하단 곡선 안티에일리어싱·접촉 그림자 | `fdc0eb67c09648b14111e71d0eac1ea24c67af4f391c66a51fc4f8de77771c80` | `b90f6132ff6e5219d159f763676a240e5391e7e1aef6428b8c9c94ea225b9c20` | 저장소 안 원본 없음 |
| `assets/motion-expanded/iot-small-tower-crane-480.webp` | 검은 판 초록 소용돌이 및 JIYOU; 다른 인쇄·알파 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 | `7163e8ce4be950e217ac49ffe5bf3e4fa1eb63211055e36f2b928533e92d30e7` | `e5cabc7a2d7fbb38323fcdf3183e64e97ab1142f24d691ade3b53bbf4aaf7274` | 저장소 안 원본 없음 |
| `assets/motion-expanded/smart-environment-board-480.webp` | 파란 판 오른쪽 위 흰 로고; 다른 인쇄·알파 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 | `6ee6c38192f379cb21839f9789ade6612530417a9798c88e8fc17804d6e7482e` | `3b94a53166d48c6f0ad01f1333aa079ee8cc961512f320016be38703f51244c2` | 저장소 안 원본 없음 |
| `assets/motion-expanded/tower-crane-hook-collision-480.webp` | 함체 스티커 전체; 제품·알파 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 | `2a61e8bfb2a4d3c7c1ab091e793b21b614e4a93041eaf9a97657c55b95c15fee` | `b19a694743f3e60dbd573c466bcffa2c5e3cdfc5c1be350e28c01fa5fc707c1e` | 저장소 안 원본 없음 |
| `assets/motion/wind-480.webp` | 함체 스티커 전체; 제품·알파 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 주변 질감 + 마스크 합성 | `ecfb6d6a45ce4d82a84e0b6dda6846f0ba580d81de6084abd592b277bff07611` | `3292cd47d612c7a7e85be625fec92d954020a1f1360d38c30877d7d63ad5346a` | 저장소 안 원본 없음 |

## 전체 파일 크기·용량 전후

픽셀 크기는 전후 동일합니다. 용량은 bytes입니다. 아래 후 용량은 원래 경로에 덮어쓴 최종 파일 기준입니다.

| 원본 파일 | 픽셀 (전후 동일) | 전 | 후 | 변화 |
|---|---:|---:|---:|---:|
| `media/derived/product-hook-bottom-camera-reference-white-20260912-480.webp` | 480×480 | 22,830 | 18,332 | -19.70% |
| `media/derived/product-hook-bottom-camera-reference-white-20260912-768.webp` | 768×768 | 43,128 | 36,516 | -15.33% |
| `media/derived/product-hook-bottom-camera-reference-white-20260912-1254.webp` | 1254×1254 | 89,566 | 79,528 | -11.21% |
| `media/derived/product-tower-crane-hook-collision-reference-white-20260912-480.webp` | 480×480 | 22,692 | 21,932 | -3.35% |
| `media/derived/product-tower-crane-hook-collision-reference-white-20260912-768.webp` | 768×768 | 46,318 | 45,320 | -2.15% |
| `media/derived/product-tower-crane-hook-collision-reference-white-20260912-1080.webp` | 1080×1080 | 80,998 | 79,882 | -1.38% |
| `media/derived/product-lte-anemometer-white-approved-20260912-480.webp` | 480×752 | 19,968 | 18,834 | -5.68% |
| `media/derived/product-lte-anemometer-white-approved-20260912-768.webp` | 768×1203 | 37,744 | 36,950 | -2.10% |
| `media/derived/product-lte-anemometer-white-approved-20260912-1002.webp` | 1002×1570 | 54,306 | 53,686 | -1.14% |
| `media/derived/product-iot-small-tower-crane-reference-white-20260912-480.webp` | 480×289 | 32,824 | 36,664 | +11.70% |
| `media/derived/product-iot-small-tower-crane-reference-white-20260912-768.webp` | 768×463 | 58,306 | 62,592 | +7.35% |
| `media/derived/product-iot-small-tower-crane-reference-white-20260912-1280.webp` | 1280×772 | 102,116 | 105,974 | +3.78% |
| `media/derived/product-smart-environment-board-reference-white-20260912-480.webp` | 480×558 | 85,924 | 95,432 | +11.07% |
| `media/derived/product-smart-environment-board-reference-white-20260912-768.webp` | 768×892 | 184,260 | 206,178 | +11.90% |
| `media/derived/product-smart-environment-board-reference-white-20260912-1280.webp` | 1280×1487 | 420,078 | 441,454 | +5.09% |
| `media/derived/product-smart-environment-board-device-480.avif` | 480×270 | 11,793 | 13,081 | +10.92% |
| `media/derived/product-smart-environment-board-device-480.webp` | 480×270 | 12,626 | 14,096 | +11.64% |
| `media/derived/product-smart-environment-board-device-768.avif` | 768×432 | 26,084 | 29,076 | +11.47% |
| `media/derived/product-smart-environment-board-device-768.webp` | 768×432 | 27,650 | 30,952 | +11.94% |
| `media/derived/product-smart-environment-board-device-1280.avif` | 1280×721 | 60,111 | 64,775 | +7.76% |
| `media/derived/product-smart-environment-board-device-1280.webp` | 1280×721 | 61,946 | 69,000 | +11.39% |
| `media/derived/product-smart-environment-board-scene-480.avif` | 480×270 | 11,783 | 13,083 | +11.03% |
| `media/derived/product-smart-environment-board-scene-480.webp` | 480×270 | 11,476 | 12,468 | +8.64% |
| `media/derived/product-smart-environment-board-scene-768.avif` | 768×432 | 24,658 | 27,607 | +11.96% |
| `media/derived/product-smart-environment-board-scene-768.webp` | 768×432 | 23,358 | 25,466 | +9.02% |
| `media/derived/product-smart-environment-board-scene-1280.avif` | 1280×721 | 53,294 | 59,687 | +12.00% |
| `media/derived/product-smart-environment-board-scene-1280.webp` | 1280×721 | 48,368 | 53,652 | +10.92% |
| `media/derived/product-smart-environment-board-scene-1600.avif` | 1600×901 | 72,149 | 80,586 | +11.69% |
| `media/derived/product-smart-environment-board-scene-1600.webp` | 1600×901 | 64,014 | 70,648 | +10.36% |
| `media/derived/product-smart-environment-board-scene-1920.avif` | 1920×1081 | 93,192 | 103,238 | +10.78% |
| `media/derived/product-smart-environment-board-scene-1920.webp` | 1920×1081 | 80,158 | 89,266 | +11.36% |
| `media/derived/product-smart-environment-board-scene-2560.avif` | 2560×1441 | 137,382 | 148,848 | +8.35% |
| `media/derived/product-smart-environment-board-scene-2560.webp` | 2560×1441 | 108,746 | 121,152 | +11.41% |
| `media/derived/product-tower-crane-hook-collision-scene-480.avif` | 480×270 | 9,974 | 10,864 | +8.92% |
| `media/derived/product-tower-crane-hook-collision-scene-480.webp` | 480×270 | 10,370 | 11,544 | +11.32% |
| `media/derived/product-tower-crane-hook-collision-scene-768.avif` | 768×432 | 18,556 | 20,711 | +11.61% |
| `media/derived/product-tower-crane-hook-collision-scene-768.webp` | 768×432 | 18,676 | 20,388 | +9.17% |
| `media/derived/product-tower-crane-hook-collision-scene-1280.avif` | 1280×720 | 36,009 | 39,549 | +9.83% |
| `media/derived/product-tower-crane-hook-collision-scene-1280.webp` | 1280×720 | 34,126 | 37,690 | +10.44% |
| `media/derived/product-tower-crane-hook-collision-scene-1600.avif` | 1600×900 | 49,175 | 53,047 | +7.87% |
| `media/derived/product-tower-crane-hook-collision-scene-1600.webp` | 1600×900 | 44,880 | 50,256 | +11.98% |
| `media/derived/product-tower-crane-hook-collision-scene-1920.avif` | 1920×1080 | 62,425 | 69,825 | +11.85% |
| `media/derived/product-tower-crane-hook-collision-scene-1920.webp` | 1920×1080 | 54,760 | 60,794 | +11.02% |
| `media/derived/product-tower-crane-hook-collision-scene-2560.avif` | 2560×1440 | 94,595 | 104,231 | +10.19% |
| `media/derived/product-tower-crane-hook-collision-scene-2560.webp` | 2560×1440 | 76,566 | 84,756 | +10.70% |
| `assets/motion-expanded/hook-bottom-camera-480.webp` | 480×480 | 27,206 | 26,872 | -1.23% |
| `assets/motion-expanded/iot-small-tower-crane-480.webp` | 480×289 | 47,968 | 53,360 | +11.24% |
| `assets/motion-expanded/smart-environment-board-480.webp` | 413×480 | 66,524 | 73,384 | +10.31% |
| `assets/motion-expanded/tower-crane-hook-collision-480.webp` | 480×480 | 32,672 | 34,576 | +5.83% |
| `assets/motion/wind-480.webp` | 306×480 | 23,944 | 24,542 | +2.50% |

## 보관용 작업 자료

- 보정본: `.jiyou-work/candidates/` 아래 원래 상대 경로와 같은 구조
- 전/후 파일별 해시·용량·압축 품질·픽셀 검사: `.jiyou-work/after.json`
- 마스크 좌표 및 무손실 중간 마스터: `.jiyou-work/masks.json`, `.jiyou-work/masters/`
- 최초 전체 출력 확대 검수판: `.jiyou-work/qa-1.png` ~ `qa-5.png` (추가 보정 16개는 `final-edge-qa-*.png`가 최종 검수판)
- 추가 경계 좌표·곡선·검수 정보: `.jiyou-work/edge-refinement.json`; 최종 적용 검증: `.jiyou-work/final-verification.json`
- 무손실 WebP 시험: hook 최대 파일 89,566 → 344,244 bytes (3.84배), scene 최대 파일 108,746 → 1,306,714 bytes (12.02배), motion_iot 47,968 → 117,442 bytes (2.45배). 이 값은 초기 보정본의 압축 방식 비교용이며 현재 후보 파일 해시와는 별도입니다.
