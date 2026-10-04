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

## 추가 처리(사이트 미사용 이미지 6종)

상태: **추가 38개 파일 원본 덮어쓰기 완료**. 기존 50개 처리 이력을 유지했으며, 누적 처리 파일은 88개입니다. 이 절의 수정 후 해시는 실제 원래 경로에 덮어쓴 파일 기준입니다.

- 가장 큰 WebP를 먼저 보정하고 Lanczos로 축소한 결과의 마스크 영역만 각 크기·형식 원본 위에 합성했습니다. 동일 사진의 AVIF도 모두 처리했습니다.
- `manual-smart-environment-board-figure-1280.webp`는 지난 작업의 `product-smart-environment-board-device-1280.webp` 수정 전 원본과 디코딩 픽셀이 완전히 같음을 확인해 검수된 국소 보정을 재사용했습니다. 수동 IoT 사진은 같은 구도지만 압축 픽셀이 달라 해당 원본에서 다시 표면 색을 추정했습니다.
- 흰 스티커는 Safety first·로고·JIYOU·주소 및 테두리를 포함해 제거했습니다. 다른 글자·숫자·아이콘·나사·케이블과 제품 형태는 편집 대상에서 제외했습니다. 특히 무선 아이콘, MODY EYE, ipTIME, 표시기 숫자·한글 영역이 마스크 밖에 있음을 좌표 검사했습니다.
- 돔 하단은 원본 곡선을 따라 약 1.7 px 안티에일리어싱과 옅은 접촉 그림자로 연결했습니다. 최초 수동 카메라 마스크의 하단이 함체 경계에 닿은 부분은 최종 적용 전에 안쪽으로 좁혀 바로잡았습니다.
- 38개 저장 전 마스크 밖 RGB 차이 0 확인. 저장 후 손실 재압축 차이는 사용자 승인 범위입니다. 전부 손실 압축이며 무손실 저장은 사용하지 않았습니다. WebP는 VP8 청크를 확인했습니다.
- 38개 모두 최종 저장 파일을 다시 열어 확대 검수했고, JIYOU·JIYOUENG·대상 소용돌이 로고·스티커 글자 잔여를 확인하지 못했습니다. 비교 이미지는 각 파일별 100%·300% 크기로 저장했습니다. 카메라 돔 경계는 별도의 300% 전후 비교로도 확인했습니다.
- 파일명·경로·픽셀 크기·형식 유지. 용량 변화 +7.76%~+11.97%로 모두 ±20% 이내. 합계 1,333,850 → 1,468,616 bytes (+10.10%).
- 이전 처리 이미지 50개는 이번 작업 전후 해시가 같습니다. HTML·CSS·JS·데이터는 변경하지 않았으며 git commit·push·branch 조작을 하지 않았습니다.

### 파일별 제거 내용·방법·SHA-256

이번 추가분은 크기·형식별 38개 파일 모두의 해시를 기록합니다.

| 원본 파일 | 지운 내용 | 방법 | 수정 전 SHA-256 | 수정 후 SHA-256 |
|---|---|---|---|---|
| `media/derived/manual-hook-bottom-camera-figure-480.avif` | 줄무늬 위 함체의 흰 스티커 전체; 노란 무선 아이콘 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `bbeb0f0ffc0977e561075a7175998f59d5402449a214ecaebf40a5490d454875` | `3a1e3dca3c61ceaf97327177be4895e1bfd7553f2b2f1bddda12a50696fe782a` |
| `media/derived/manual-hook-bottom-camera-figure-480.webp` | 줄무늬 위 함체의 흰 스티커 전체; 노란 무선 아이콘 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `d375421cc17377a89afe789fe236209871b4f5b516466976b2310a3f06f94568` | `fe19d2ed623cc8e6f37c9cca5204633e544f25d981f47d3a4993c6dfe01b2275` |
| `media/derived/manual-hook-bottom-camera-figure-768.avif` | 줄무늬 위 함체의 흰 스티커 전체; 노란 무선 아이콘 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `a569a66d543728dc598db2d80ef9c217e3a6d3189cb6f9222160f7d7cae57b31` | `9fbb3c0eb989769eceb5584c7911be4c677960c2c23db6a1c49bb0fe533cf328` |
| `media/derived/manual-hook-bottom-camera-figure-768.webp` | 줄무늬 위 함체의 흰 스티커 전체; 노란 무선 아이콘 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `8ceae9e1b1665d687ba8ee11777f71fc28a80f5ed2b0405d400bd3ceeb3bc13e` | `0661647a7021eea78835808427535aa5ee2455ae7ff9305bd5bf0fc004a3ba52` |
| `media/derived/manual-iot-small-tower-crane-figure-480.avif` | 검은 표시기 왼쪽 초록 소용돌이·JIYOU; 나머지 아이콘·숫자·한글 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 | `2e42b83b84bdbc21459de090a8aff51f586ae7a3154bcb0590d6fa31af2da8ee` | `9a1325556a11b1e535def44e692a9f901b5ad5f15e8a7b7f7c7726a5cab1cd5f` |
| `media/derived/manual-iot-small-tower-crane-figure-480.webp` | 검은 표시기 왼쪽 초록 소용돌이·JIYOU; 나머지 아이콘·숫자·한글 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 | `75a36852c5c3c6c61636615cdaa6f41ddd4e212a4aaaa088d00db90b0381ba55` | `9005411853031eda1ee28e22c6c836e1c305e1c37b16105feaf840d09878cd2a` |
| `media/derived/manual-iot-small-tower-crane-figure-768.avif` | 검은 표시기 왼쪽 초록 소용돌이·JIYOU; 나머지 아이콘·숫자·한글 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 | `ddd7e38b867122b969df02a7cea5db1381f4399e621d7231d65bedde2d0551dd` | `a7b5f8e9bde3f419c1fd290d41d015705d8850bacf13cb18b921704e74827659` |
| `media/derived/manual-iot-small-tower-crane-figure-768.webp` | 검은 표시기 왼쪽 초록 소용돌이·JIYOU; 나머지 아이콘·숫자·한글 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 | `d832e44fc386a024be065fe69325a9c807893de2bbc45cb05dfb386e288b3bd1` | `d296c7c5def508affe4a9378343f63042513e42eb46d75139aba0133a60694fb` |
| `media/derived/manual-iot-small-tower-crane-figure-1280.avif` | 검은 표시기 왼쪽 초록 소용돌이·JIYOU; 나머지 아이콘·숫자·한글 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 | `aa954d0cdf455bb8231c0f27e7a765e1747b13f8720e0293110e3bf5f734acf8` | `052b3e5f1c91f3ebbcc5a5eebce2684c80b79e296fa0a39b784df85b79151d4d` |
| `media/derived/manual-iot-small-tower-crane-figure-1280.webp` | 검은 표시기 왼쪽 초록 소용돌이·JIYOU; 나머지 아이콘·숫자·한글 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 | `128997d1ae8bf4013c66be07df255980f7af786625135e1407a9713d7806bb63` | `340440625d8e88256830c2c862c72ae71abc489eaf741a0b877e34c7b098b92e` |
| `media/derived/manual-smart-environment-board-figure-480.avif` | 옥상 전광판 우상단 로고, 기둥 함체 상단 스티커·하단 로고 라벨 | 픽셀 일치 원본의 기존 검수 보정 마스터 재사용 + 크기별 마스크 합성 | `302b48eda25684f3bb7d488bca0bd2c1524bc1ee0349043519bc292d7c63bda2` | `3bf092f001f6bdb66800e16f7a3914faa04d2408368697f0b89fa2ad8689fef8` |
| `media/derived/manual-smart-environment-board-figure-480.webp` | 옥상 전광판 우상단 로고, 기둥 함체 상단 스티커·하단 로고 라벨 | 픽셀 일치 원본의 기존 검수 보정 마스터 재사용 + 크기별 마스크 합성 | `9c619bb1b56322d2129b0f5c2351244040e75ef091d750a05e1bf209bb8e8fc9` | `0635ca4f9d5ae1028e0991fcf5dfdda660440d52d6f03aa02f625b40686bbd7a` |
| `media/derived/manual-smart-environment-board-figure-768.avif` | 옥상 전광판 우상단 로고, 기둥 함체 상단 스티커·하단 로고 라벨 | 픽셀 일치 원본의 기존 검수 보정 마스터 재사용 + 크기별 마스크 합성 | `cbd4c2d78eb82ed264519b1f1cc15f0a3c7580fca295b44b77801f97cc1cac3e` | `0ed25d9824277d0c2c6a778a440bd90ed700d51f7d2235134bd318b21bb0f7fc` |
| `media/derived/manual-smart-environment-board-figure-768.webp` | 옥상 전광판 우상단 로고, 기둥 함체 상단 스티커·하단 로고 라벨 | 픽셀 일치 원본의 기존 검수 보정 마스터 재사용 + 크기별 마스크 합성 | `3592bc793bf8f74b62a5cde5d57f945af84e9fed5eec5d7fae4b50063fbaf4bd` | `f8b140a23867e4fe3a409b7ea50d0196256aa83ed21217e3030b7ee8b539b48e` |
| `media/derived/manual-smart-environment-board-figure-1280.avif` | 옥상 전광판 우상단 로고, 기둥 함체 상단 스티커·하단 로고 라벨 | 픽셀 일치 원본의 기존 검수 보정 마스터 재사용 + 크기별 마스크 합성 | `76a9a3e8ca93b2cb9fa572a5d188da65526e676eeb8a07eea0e9e2272369de2c` | `c7c564c0b170493e05469b7547a7249c2832379236d223654cf8f483ccfa2248` |
| `media/derived/manual-smart-environment-board-figure-1280.webp` | 옥상 전광판 우상단 로고, 기둥 함체 상단 스티커·하단 로고 라벨 | 픽셀 일치 원본의 기존 검수 보정 마스터 재사용 + 크기별 마스크 합성 | `93767edc136a6f93143dacb250c37eada794fe44207775c67d45a749b29a16c5` | `a0f605ec7ed74fabd5cb87b8bc594f8d9d97726956b4c74393a07f3cdc6b5642` |
| `media/derived/product-hook-bottom-camera-device-480.avif` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `77015ac3f2e5a5e9ae389f01aea391260dbfc5a3d4963b121d3eaf3453ff51a9` | `079820c228cb75d8d228f282e849b04c124127390e8f3392d55e3dec3a1711d2` |
| `media/derived/product-hook-bottom-camera-device-480.webp` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `4f82b1029423cb5f77fb1492a16078bba063e30531340c354b52c3918692e3d2` | `00dfbbd6fd562bdae36e9454344d9c9e68b4799546cd2da82712e35ea2df9ea8` |
| `media/derived/product-hook-bottom-camera-device-768.avif` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `fa2364cd9c14b071f14691be13b7edee99ae29b3954cedb2213b08e7f4ada4b8` | `f1a8c8149d663d4e78b85c476c5c22c0b6c9a150156570ac781cf12db844e691` |
| `media/derived/product-hook-bottom-camera-device-768.webp` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `a3a3111dbbab20c4abc8f664efa12f1ce7a789b5b5e2d6ee0b096832fc65795c` | `16b672a932e296196fff76ba2b8727be67d45c2ca598067dc137cc203103e7e6` |
| `media/derived/product-hook-bottom-camera-device-1280.avif` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `0c178320bcf93a513987192909779df3d46fead21e367e8566ba9e8c0343cd3f` | `1db581dc97f16bf7d2cc0b7d8ef23afe406dea8dc5c3d02b30ea4a72cd0939b9` |
| `media/derived/product-hook-bottom-camera-device-1280.webp` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `925c33122eb538696071982e3dce245605bc221b6715b252d6c31a9306e214bc` | `be5d730a6e979ac4d92b69828c3b7ad1cd72a53187cac7fc1d3f9535574b8297` |
| `media/derived/product-hook-bottom-camera-scene-480.avif` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `6a0614b8503481865a8459c0ad8dd1ee3b110516049cdc83e288a4ffc4b8084d` | `5caa77b49456bf6f0b8252e38ef5174b262d60b8602fbac07877927f626a571f` |
| `media/derived/product-hook-bottom-camera-scene-480.webp` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `273fa74bb7ac40288c4db77884e168ed0a83c3c75a4dd52ce0e9a0dfe137a3cb` | `e3b1805b432ede2308c1f7dc6ff98557e695977f3d2df3809c6945db4212c7fa` |
| `media/derived/product-hook-bottom-camera-scene-768.avif` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `3105175c68e5230fed38ffc02ca44d950b31ad23b890a89410d466e6863b819c` | `c6d064ea28e6c741d0f642de1d26a3d4522eb0ec1354ac936b42a21ea1c248f5` |
| `media/derived/product-hook-bottom-camera-scene-768.webp` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `50fa6cf27fb64886462f69485cbbec7e9ee095539c9f1f64f9ce940642e40495` | `c504921f1d280ca88daf7b9efae3426de4e04978a5e8de47e78b78926a40aeb4` |
| `media/derived/product-hook-bottom-camera-scene-1280.avif` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `b5eb8134abf89ce502462c24a2fdeeaa41b6c570363c07efe010e091f28e87e7` | `127695b2df3d16faecef321a0481a43f4562ae10e8476633334038ab5b5128e6` |
| `media/derived/product-hook-bottom-camera-scene-1280.webp` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `aaa03dc24c8de2c0d5cd26d126785bce288220217e94f7d40b57ba2e2631db79` | `e4bba34169f1f7b740a9bea45e6dbc142eed372d86d6a6f48d1b83fc720150aa` |
| `media/derived/product-hook-bottom-camera-scene-1600.avif` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `39ccc9136aa6f00b5ed893827108dff30e7e037ac70c0e1566ce575577bb72c8` | `ec1c641e96da763e8c51f2f02fd49a46b7c4ff76a6955aa7361c04ea208ad2de` |
| `media/derived/product-hook-bottom-camera-scene-1600.webp` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `f23cab938b35e9c452970c8cf4209a5a526988698f68efb66a09610a72dbaad5` | `6ac6f3a8f93d33b45410a3b399cc636cc2b59de9659aa194057b505cef3aac54` |
| `media/derived/product-hook-bottom-camera-scene-1920.avif` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `7fa1b010689ca4a56b1e9166f8db8217b4cb6cec8108adb38ad1446ce7583ed0` | `e5dc6a267dad532e03815e8f95d155664e815c2bf01b8c8bdae2fbb3c29cfa76` |
| `media/derived/product-hook-bottom-camera-scene-1920.webp` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `cf009e43568b3871b5b5187628dac4a7c88d9f2059ca3ac9530f65f29c495bb5` | `191cccbe97bfc6c4f21ae2179ab50458887bcb938277af89a86a9632806e1fd6` |
| `media/derived/product-hook-bottom-camera-scene-2560.avif` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `0ef5c97b41f3441f23b2fcdf160ecf468091240fd3a5358fc6821c46b74dea22` | `1934a09a19a569046c569d7a418009aa0099f6e5f657557d440cc069e12aa42e` |
| `media/derived/product-hook-bottom-camera-scene-2560.webp` | 함체 흰 스티커 전체; MODY EYE·ipTIME 보존 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 + 돔 경계 안티에일리어싱·옅은 접촉 그림자 | `230c041c153a5b1de34d73117e9e49b9fc35bce403ade88a306b6df901c42035` | `644c037b205970028c732a699065b289ec3a55cc5e3d9c98f5a173f07b828bcb` |
| `media/derived/product-mobile-cctv-max-studio-480.avif` | 초록 기둥 중간 함체의 작은 로고·JIYOU 표시 전체 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 | `ab6e0aa591a1b034982d3eecc3b0ac347c73e9cf7c58278da56596ade0d01dbf` | `00680c8a04be250306aac3664bfdde9c174fe2de567b1cb32e5516189a72f402` |
| `media/derived/product-mobile-cctv-max-studio-480.webp` | 초록 기둥 중간 함체의 작은 로고·JIYOU 표시 전체 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 | `ea17f46bccc995f85ab4d52e2e266c7b784233fc88aa07f77a0363c01a4ac9f2` | `072cb68c755884a4d1942b0d2dc6d082c16eab46fb6e937077bfeef786b4aef4` |
| `media/derived/product-mobile-cctv-max-studio-768.avif` | 초록 기둥 중간 함체의 작은 로고·JIYOU 표시 전체 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 | `4b7d57ab933e42ac3a2380df9bda89536a51b90d9ff99e9f41af073ac7e97111` | `673a209f01e639a26baaf89ac6951fff3f24fe857fc45d9a577ea04efc90793c` |
| `media/derived/product-mobile-cctv-max-studio-768.webp` | 초록 기둥 중간 함체의 작은 로고·JIYOU 표시 전체 | Pillow/NumPy 국소 다항 표면 복원 인페인팅 + 마스크 합성 | `053f027d0894298a760a46c9b0925dd60f00e5e538bfa833f3d96917416d2d91` | `31a424cc85ef9bc1e4fa248e93f37d0a002c290f4157eecd267d925de76a9772` |

### 파일별 픽셀 크기·용량 전후

픽셀 크기는 전후 동일하며, 용량은 bytes입니다.

| 파일 | 픽셀 크기 | 전 | 후 | 변화 |
|---|---:|---:|---:|---:|
| `media/derived/manual-hook-bottom-camera-figure-480.avif` | 480×537 | 11,297 | 12,366 | +9.46% |
| `media/derived/manual-hook-bottom-camera-figure-480.webp` | 480×537 | 10,226 | 11,392 | +11.40% |
| `media/derived/manual-hook-bottom-camera-figure-768.avif` | 768×860 | 19,859 | 21,926 | +10.41% |
| `media/derived/manual-hook-bottom-camera-figure-768.webp` | 768×860 | 17,148 | 19,168 | +11.78% |
| `media/derived/manual-iot-small-tower-crane-figure-480.avif` | 480×289 | 12,009 | 13,059 | +8.74% |
| `media/derived/manual-iot-small-tower-crane-figure-480.webp` | 480×289 | 10,630 | 11,800 | +11.01% |
| `media/derived/manual-iot-small-tower-crane-figure-768.avif` | 768×463 | 20,061 | 21,725 | +8.29% |
| `media/derived/manual-iot-small-tower-crane-figure-768.webp` | 768×463 | 17,672 | 19,726 | +11.62% |
| `media/derived/manual-iot-small-tower-crane-figure-1280.avif` | 1280×772 | 32,963 | 36,062 | +9.40% |
| `media/derived/manual-iot-small-tower-crane-figure-1280.webp` | 1280×772 | 31,916 | 35,646 | +11.69% |
| `media/derived/manual-smart-environment-board-figure-480.avif` | 480×270 | 11,793 | 13,081 | +10.92% |
| `media/derived/manual-smart-environment-board-figure-480.webp` | 480×270 | 12,626 | 14,096 | +11.64% |
| `media/derived/manual-smart-environment-board-figure-768.avif` | 768×432 | 26,084 | 29,076 | +11.47% |
| `media/derived/manual-smart-environment-board-figure-768.webp` | 768×432 | 27,650 | 30,952 | +11.94% |
| `media/derived/manual-smart-environment-board-figure-1280.avif` | 1280×721 | 60,111 | 64,775 | +7.76% |
| `media/derived/manual-smart-environment-board-figure-1280.webp` | 1280×721 | 61,946 | 69,000 | +11.39% |
| `media/derived/product-hook-bottom-camera-device-480.avif` | 480×640 | 24,061 | 26,787 | +11.33% |
| `media/derived/product-hook-bottom-camera-device-480.webp` | 480×640 | 25,084 | 27,960 | +11.47% |
| `media/derived/product-hook-bottom-camera-device-768.avif` | 768×1024 | 48,344 | 53,513 | +10.69% |
| `media/derived/product-hook-bottom-camera-device-768.webp` | 768×1024 | 46,374 | 51,924 | +11.97% |
| `media/derived/product-hook-bottom-camera-device-1280.avif` | 1280×1707 | 103,466 | 112,384 | +8.62% |
| `media/derived/product-hook-bottom-camera-device-1280.webp` | 1280×1707 | 89,254 | 99,424 | +11.39% |
| `media/derived/product-hook-bottom-camera-scene-480.avif` | 480×270 | 10,849 | 12,065 | +11.21% |
| `media/derived/product-hook-bottom-camera-scene-480.webp` | 480×270 | 10,866 | 12,112 | +11.47% |
| `media/derived/product-hook-bottom-camera-scene-768.avif` | 768×432 | 19,865 | 22,051 | +11.00% |
| `media/derived/product-hook-bottom-camera-scene-768.webp` | 768×432 | 19,418 | 21,336 | +9.88% |
| `media/derived/product-hook-bottom-camera-scene-1280.avif` | 1280×720 | 39,308 | 42,753 | +8.76% |
| `media/derived/product-hook-bottom-camera-scene-1280.webp` | 1280×720 | 37,140 | 41,520 | +11.79% |
| `media/derived/product-hook-bottom-camera-scene-1600.avif` | 1600×900 | 53,058 | 57,297 | +7.99% |
| `media/derived/product-hook-bottom-camera-scene-1600.webp` | 1600×900 | 48,192 | 53,886 | +11.82% |
| `media/derived/product-hook-bottom-camera-scene-1920.avif` | 1920×1081 | 67,913 | 75,584 | +11.30% |
| `media/derived/product-hook-bottom-camera-scene-1920.webp` | 1920×1081 | 60,050 | 65,346 | +8.82% |
| `media/derived/product-hook-bottom-camera-scene-2560.avif` | 2560×1441 | 104,907 | 113,150 | +7.86% |
| `media/derived/product-hook-bottom-camera-scene-2560.webp` | 2560×1441 | 83,376 | 91,886 | +10.21% |
| `media/derived/product-mobile-cctv-max-studio-480.avif` | 480×853 | 9,370 | 10,134 | +8.15% |
| `media/derived/product-mobile-cctv-max-studio-480.webp` | 480×853 | 10,824 | 11,752 | +8.57% |
| `media/derived/product-mobile-cctv-max-studio-768.avif` | 768×1365 | 18,018 | 19,684 | +9.25% |
| `media/derived/product-mobile-cctv-max-studio-768.webp` | 768×1365 | 20,122 | 22,218 | +10.42% |

### 추가 작업 기록

- 전/후 비교: `.jiyou-work/rest/comparisons/<원래 파일명>-100.png`, `-300.png` (38개 파일 × 2배율)
- 최종 확대 검수판: `.jiyou-work/rest/qa-1.png` ~ `qa-4.png`
- 수정 전 백업: `.jiyou-work/rest/originals/`
- 마스크 및 보정 마스터: `.jiyou-work/rest/masks.json`, `.jiyou-work/rest/masters/`
- 전후 해시·용량·압축 품질: `.jiyou-work/rest/before.json`, `after.json`
- 최종 적용 검증: `.jiyou-work/rest/final-verification.json`
- `.jiyou-work/` 전체는 작업 기록으로 보존하고 Git 스테이징에 추가하지 않았습니다.

## 추가 처리 2

- 추가 작업 3: `assets/motion/cameraM-480.webp` — 흰 함체 스티커 전체(Safety first·로고·JIYOU·주소·테두리)를 Pillow/NumPy 국소 1차 표면 복원 인페인팅과 0.6 px 가장자리 블렌딩으로 제거, 마스크 영역만 합성하여 **원본 덮어쓰기 완료**. 360×480 WebP·알파 채널 유지(알파 차이 0), 저장 전 마스크 밖 차이 0, 손실 압축 q98·재압축 차이 허용, 22,106 → 24,660 bytes(+11.55%). 100%·300% 확대 확인 완료. 수정 전 SHA-256 `876e6ea834758609451a5a87742775d58d8ea17b516f2eab47a75aa43a25163d`, 수정 후 `ba1926ef95fb420095281ae6f24acfcad55ce807b68b3ed5f6e79382c0e2a5ec`. 전후 비교·백업·검증 기록: `.jiyou-work/more/cameraM/`. 이 절 총 13개, 누적 101개 처리.

상태: **추가 12개 파일 원본 덮어쓰기 완료**. 기존 88개 처리 이력을 유지했으며 누적 처리 파일은 100개입니다. 수정 후 해시는 원래 경로에 덮어쓴 최종 파일 기준입니다.

- 각 묶음의 가장 큰 768 px WebP를 먼저 보정하고 Lanczos로 축소했습니다. 크기·형식별 원본 위에 해당 마스크 영역만 합성했으며 AVIF도 모두 처리했습니다.
- 함체 스티커는 테두리까지 제거하고 주변 함체의 색·조명으로 복원했습니다. 부품·나사·함체 경계는 마스크에서 제외했고 편집 가장자리를 부드럽게 연결했습니다. 새 로고나 글자는 넣지 않았습니다.
- 표지는 같은 원본에서 수직 격자 위치와 수평 격자 주기가 맞는 남색 배경을 복제했습니다. MOVING, SAFETY FIRST, 색 막대와 하단 글자, 원형 아이콘은 마스크 밖에 있음을 확인했습니다.
- 12개 모두 저장 전 마스크 밖 RGB 차이 0을 확인했습니다. 저장 후 손실 재압축에 따른 마스크 밖 미세 차이는 사용자 승인 범위입니다. 모든 출력은 손실 압축이며 무손실 저장을 사용하지 않았습니다. WebP는 VP8 청크를 확인했습니다.
- 최종 인코딩한 12개 파일의 수정 영역을 확대 검수했고 JIYOU·대상 로고·스티커 글자 잔여를 발견하지 못했습니다. 파일별 100%·300% 전후 비교를 저장했습니다.
- 파일명·경로·픽셀 크기·형식을 유지했습니다. 용량 변화는 +6.30%~+11.35%로 모두 ±20% 이내입니다. 합계 86,733 → 94,462 bytes (+8.91%).
- 이전 처리 이미지 88개는 이번 작업 전후 해시가 같습니다. HTML·CSS·JS·데이터는 변경하지 않았으며 git commit·push·branch 조작을 하지 않았습니다.

### 파일별 제거 내용·방법·SHA-256

| 원본 파일 | 지운 내용 | 방법 | 수정 전 SHA-256 | 수정 후 SHA-256 |
|---|---|---|---|---|
| `media/derived/product-movingcam-m-480.avif` | 초록 기둥 아래 흰 함체의 흰 스티커 전체(Safety first·로고·JIYOU·주소·테두리) | Pillow/NumPy 국소 1차 표면 복원 인페인팅 + 1 px 가장자리 블렌딩 + 크기별 원본 마스크 합성 | `a22245b8962a1537acab70728ff76eaab1f7fec0686afe7789edb8a4ceb32cde` | `dd85803a26a7816212e8dd2bb27548eaca1c4888e4f4c436ba058b3c9c8ec91f` |
| `media/derived/product-movingcam-m-480.webp` | 초록 기둥 아래 흰 함체의 흰 스티커 전체(Safety first·로고·JIYOU·주소·테두리) | Pillow/NumPy 국소 1차 표면 복원 인페인팅 + 1 px 가장자리 블렌딩 + 크기별 원본 마스크 합성 | `57d29d67dc950eed88a85cb00f64c658fcd96b32be6028ac108d6dcb1391605a` | `36e8422d583e377edb6b563426121a820ea99c3c65015c77713f226f7a78dcb6` |
| `media/derived/product-movingcam-m-768.avif` | 초록 기둥 아래 흰 함체의 흰 스티커 전체(Safety first·로고·JIYOU·주소·테두리) | Pillow/NumPy 국소 1차 표면 복원 인페인팅 + 1 px 가장자리 블렌딩 + 크기별 원본 마스크 합성 | `07a4a3a8a3cd6ae4fb589854b0701ba99b757f4d0b2b1396cbbfb09ccc7fafb7` | `014ea2d6ac8c99396bc00d0acc39bbac6f218a2cec019012b48f6424983d3b3a` |
| `media/derived/product-movingcam-m-768.webp` | 초록 기둥 아래 흰 함체의 흰 스티커 전체(Safety first·로고·JIYOU·주소·테두리) | Pillow/NumPy 국소 1차 표면 복원 인페인팅 + 1 px 가장자리 블렌딩 + 크기별 원본 마스크 합성 | `5ddb0433bef2861e458f79b4b857a012eddb5fec76d97b53ca4b7f05d6c296d4` | `9a557f034478a2b894f1664c83eae2aa1f7df80a5af4d95fb0bccfbe66441a56` |
| `media/derived/manual-lte-anemometer-figure-480.avif` | 함체 흰 스티커 전체(Safety first·로고·JIYOU·주소·테두리) | Pillow/NumPy 국소 2차 표면 복원 인페인팅 + 1.4 px 가장자리 블렌딩 + 크기별 원본 마스크 합성 | `a886257c5a58a5aabe9f120522fc0f677d5bf7f896d9542310a64ff2c0287a2a` | `f87910803c963b229e9920b5eed5947c713f89eccba61fde5a857c09dd353b09` |
| `media/derived/manual-lte-anemometer-figure-480.webp` | 함체 흰 스티커 전체(Safety first·로고·JIYOU·주소·테두리) | Pillow/NumPy 국소 2차 표면 복원 인페인팅 + 1.4 px 가장자리 블렌딩 + 크기별 원본 마스크 합성 | `e4a425d72828954671bf4a7a891edb55cccb6c9dba9db80cd0b416ea68b6bd4f` | `3e0db9071723616bf865548b5341f94ad89cde310341033cab6ed9ec79924cd7` |
| `media/derived/manual-lte-anemometer-figure-768.avif` | 함체 흰 스티커 전체(Safety first·로고·JIYOU·주소·테두리) | Pillow/NumPy 국소 2차 표면 복원 인페인팅 + 1.4 px 가장자리 블렌딩 + 크기별 원본 마스크 합성 | `c451f829b75af2defb6ca6e940d277fb640edb79c621da9db8f003c0fa5978b5` | `b09434b6130d8a005e569c85f6ac5c6cfb5eaf2d086279e37d1428d0b146c429` |
| `media/derived/manual-lte-anemometer-figure-768.webp` | 함체 흰 스티커 전체(Safety first·로고·JIYOU·주소·테두리) | Pillow/NumPy 국소 2차 표면 복원 인페인팅 + 1.4 px 가장자리 블렌딩 + 크기별 원본 마스크 합성 | `2728a0132632c8ee2237977c79f2d1de3b87dd9ecff1103aecf326e6831125d5` | `aa9b738772ec430104003f6673d0294b38cc84355ab5fbb54f9538db92d9fb33` |
| `media/derived/moving-cover-480.avif` | 남색 표지 오른쪽 아래 JIYOU 로고 아이콘·글자 | 같은 원본의 격자 위상을 맞춘 배경 복제 인페인팅(y 오프셋 173 px) + 1.1 px 가장자리 블렌딩 + 크기별 원본 마스크 합성 | `df8f8213daccfafca7af156f0fd686a907c1dd8facc32947f976cacf49d49190` | `379f65a223dc9a17f7f29444ada867d6d4035bfb568bd5dc0d3ca711fc73c6fd` |
| `media/derived/moving-cover-480.webp` | 남색 표지 오른쪽 아래 JIYOU 로고 아이콘·글자 | 같은 원본의 격자 위상을 맞춘 배경 복제 인페인팅(y 오프셋 173 px) + 1.1 px 가장자리 블렌딩 + 크기별 원본 마스크 합성 | `b1509862bcc3efdc85e3168f4ec7f382abcd61b1e9a3e05be9d5baeaf28ce2a4` | `d49777743b2621c19a66b59b5f275497a355dfa14a81e3fc278209d2613a5f77` |
| `media/derived/moving-cover-768.avif` | 남색 표지 오른쪽 아래 JIYOU 로고 아이콘·글자 | 같은 원본의 격자 위상을 맞춘 배경 복제 인페인팅(y 오프셋 173 px) + 1.1 px 가장자리 블렌딩 + 크기별 원본 마스크 합성 | `225456aaa5d401f76912da258f3d2d25f8a78f05ac1a35617dd9ae5e50bbe667` | `80bdb02464270ff720c28e4ad749422183dc77351712e4b5f966076f94952f27` |
| `media/derived/moving-cover-768.webp` | 남색 표지 오른쪽 아래 JIYOU 로고 아이콘·글자 | 같은 원본의 격자 위상을 맞춘 배경 복제 인페인팅(y 오프셋 173 px) + 1.1 px 가장자리 블렌딩 + 크기별 원본 마스크 합성 | `7425fe91b9436fe85309f8e0607e3c8bd6af6da9ff70803fd28cc1f98e068e08` | `71c2410467a40eb323c5324fc38f34fbd70a283e3b47105e892a3c3cc2f30e8b` |

### 파일별 픽셀 크기·용량 전후

픽셀 크기는 전후 동일하며 용량은 bytes입니다.

| 파일 | 픽셀 크기 | 전 | 후 | 변화 |
|---|---:|---:|---:|---:|
| `media/derived/product-movingcam-m-480.avif` | 480×640 | 6,355 | 7,076 | +11.35% |
| `media/derived/product-movingcam-m-480.webp` | 480×640 | 6,470 | 7,156 | +10.60% |
| `media/derived/product-movingcam-m-768.avif` | 768×1024 | 11,276 | 12,466 | +10.55% |
| `media/derived/product-movingcam-m-768.webp` | 768×1024 | 12,316 | 13,414 | +8.92% |
| `media/derived/manual-lte-anemometer-figure-480.avif` | 480×753 | 6,712 | 7,212 | +7.45% |
| `media/derived/manual-lte-anemometer-figure-480.webp` | 480×753 | 5,812 | 6,178 | +6.30% |
| `media/derived/manual-lte-anemometer-figure-768.avif` | 768×1204 | 10,508 | 11,405 | +8.54% |
| `media/derived/manual-lte-anemometer-figure-768.webp` | 768×1204 | 10,534 | 11,226 | +6.57% |
| `media/derived/moving-cover-480.avif` | 480×270 | 3,335 | 3,604 | +8.07% |
| `media/derived/moving-cover-480.webp` | 480×270 | 2,998 | 3,242 | +8.14% |
| `media/derived/moving-cover-768.avif` | 768×433 | 5,371 | 5,889 | +9.64% |
| `media/derived/moving-cover-768.webp` | 768×433 | 5,046 | 5,594 | +10.86% |

### 추가 작업 2 기록

- 전후 비교: `.jiyou-work/more/comparisons/<원래 파일명>-100.png`, `-300.png` (12개 파일 × 2배율)
- 최종 확대 검수판: `.jiyou-work/more/qa-1.png` ~ `qa-3.png`
- 수정 전 백업: `.jiyou-work/more/originals/`
- 마스크·보정 마스터: `.jiyou-work/more/masks.json`, `masters/`
- 전후 해시·용량·압축 품질: `.jiyou-work/more/before.json`, `after.json`
- 최종 적용 검증: `.jiyou-work/more/final-verification.json`
- `.jiyou-work/`는 작업 기록으로 보존했으며 Git 스테이징에 추가하지 않았습니다.
