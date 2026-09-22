"""Readable buyer explanation beside the unmodified source screenshot."""
from bs4 import BeautifulSoup

def refine_proof(s, root, slug):
 if slug != 'chatgpt-cctv': return
 proof=root.select_one('.revision-proof')
 if not proof or proof.select_one('.buyer-report-layout'):return
 proof['id']='report-preview'
 proof['class']=proof.get('class',[])+['buyer-report-proof']
 inner=proof.select_one('.editorial-section-inner')
 inner.find('h2').string='현장 장면에서 보고서 초안까지.'
 inner.select_one('.editorial-kicker').string='도입 후의 검토 흐름'
 source=inner.find('a',recursive=False).extract()
 source['class']=['buyer-report-source']
 source.select_one('span').string='제품 자료 원본 보기 ↗'
 fragment=BeautifulSoup('''<p class="buyer-report-lead">AI가 정리한 초안을 현장 영상과 대조해 검토합니다. 최종 판단은 안전관리자가 맡습니다.</p>
 <div class="buyer-report-layout">
 <figure class="buyer-report-reference"><figcaption>제품 자료에 담긴 화면</figcaption></figure>
 <div class="buyer-report-explanation"><h3>무엇을 확인할 수 있나요?</h3>
 <ol class="buyer-report-steps">
 <li><span aria-hidden="true">01</span><div><h4>보고할 장면을 선택</h4><p>CCTV 목록에서 확인할 현장과 영상 장면을 고릅니다.</p></div></li>
 <li><span aria-hidden="true">02</span><div><h4>AI 보고서 초안을 확인</h4><p>선택한 장면의 관찰 내용과 위험요인 초안을 살펴봅니다.</p></div></li>
 <li><span aria-hidden="true">03</span><div><h4>장면과 대조해 검토</h4><p>안전관리자가 현장 상황과 맞는지 확인하고, 추가로 살펴볼 내용을 판단합니다.</p></div></li>
 </ol>
 <p class="buyer-report-outcome"><strong>구매 전 확인할 점</strong>현장에서 사용할 CCTV 구성과 보고서 검토 방식을 상담 시 함께 확인하세요.</p>
 </div></div>''','html.parser')
 fragment.select_one('.buyer-report-reference').insert(0,source)
 inner.append(fragment)
