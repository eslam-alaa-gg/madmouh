from bs4 import BeautifulSoup
from urllib.request import urlopen
from pathlib import Path
import base64
import re

logo_source = Path("assets/wisal-logo.jpg.b64")
if logo_source.exists():
    Path("img").mkdir(parents=True, exist_ok=True)
    logo_bytes = base64.b64decode(logo_source.read_text().strip())
    if not logo_bytes:
        raise RuntimeError("Wisal logo file is empty")
    Path("img/wisal-logo.jpg").write_bytes(logo_bytes)

SOURCE_URL = "https://sadakah-58j1.vercel.app/"
try:
    source = urlopen(SOURCE_URL, timeout=30).read().decode("utf-8")
except Exception:
    source = urlopen("https://raw.githubusercontent.com/eslam-alaa-gg/sadakah/main/index.html", timeout=30).read().decode("utf-8")

soup = BeautifulSoup(source, "html.parser")
if not soup.find("main"):
    raise RuntimeError("The reference page could not be parsed.")

soup.html["data-theme"] = "light"
if soup.title:
    soup.title.string = "صدقة جارية على روح ممدوح"

for meta in list(soup.find_all("meta")):
    if meta.get("name") == "visitors-api":
        meta.decompose()
        continue
    if meta.get("name") == "theme-color":
        meta["content"] = "#F8F6F3"
    if meta.get("name") == "description":
        meta["content"] = "صدقة جارية على روح ممدوح — قرآن كريم، أدعية مأثورة، أذكار ومسبحة إلكترونية وأسماء الله الحسنى."
    if meta.get("property") == "og:title":
        meta["content"] = "صدقة جارية على روح ممدوح"
    if meta.get("property") == "og:description":
        meta["content"] = "قرآن كريم، أدعية وأذكار ومسبحة إلكترونية وأسماء الله الحسنى."
    if meta.get("property") == "og:url":
        meta["content"] = "https://madmouh.vercel.app/"
    if meta.get("property") == "og:image":
        meta["content"] = "https://madmouh.vercel.app/img/photo.jpg"
    if meta.get("name") == "twitter:title":
        meta["content"] = "صدقة جارية على روح ممدوح"
    if meta.get("name") == "twitter:description":
        meta["content"] = "قرآن كريم، أدعية وأذكار ومسبحة إلكترونية وأسماء الله الحسنى."
    if meta.get("name") == "twitter:image":
        meta["content"] = "https://madmouh.vercel.app/img/photo.jpg"

main = soup.find("main")
for node in list(main.find_all(recursive=False)):
    if node.name == "header" and node.get("id") == "home":
        node.decompose()
    elif node.name == "section" and "mem" in (node.get("class") or []):
        node.decompose()

hero = soup.new_tag("header", id="home")
hero["class"] = ["mamdouh-intro"]
inner = soup.new_tag("div")
inner["class"] = ["mamdouh-intro-inner"]
photo = soup.new_tag("img", src="img/photo.jpg", alt="صورة ممدوح", loading="eager", width="368", height="716")
photo["class"] = ["mamdouh-photo"]
name = soup.new_tag("h1")
name["class"] = ["mamdouh-name"]
name.string = "ممدوح"
subtitle = soup.new_tag("p")
subtitle["class"] = ["mamdouh-subtitle"]
subtitle.string = "اللهم اغفر له وارحمه واجعل قبره روضةً من رياض الجنة"
inner.extend([photo, name, subtitle])
hero.append(inner)
main.insert(0, hero)

toolbar = soup.new_tag("div", id="mamdouh-toolbar")
toolbar["class"] = ["mamdouh-toolbar"]
brand = soup.new_tag("a", href="#home", id="mamdouh-brand")
brand["aria-label"] = "وصال"
brand_img = soup.new_tag("img", src="img/wisal-logo.jpg", alt="وصال", width="104", height="48", loading="eager")
brand.append(brand_img)
toolbar.append(brand)
main.insert_before(toolbar)

visitor = soup.new_tag("div", id="mamdouh-visitor-counter")
visitor["class"] = ["mamdouh-visitor-counter"]
visitor["role"] = "status"
visitor["aria-live"] = "polite"
visitor_label = soup.new_tag("span")
visitor_label.string = "زيارات تقديرية"
visitor_num = soup.new_tag("strong", id="mamdouh-visitor-count")
visitor_num.string = "—"
visitor.extend([visitor_label, visitor_num])
toolbar.insert_after(visitor)

dua_section = soup.find("section", id="dua")
praised_section = soup.find("section", id="praised")
hadith_section = soup.find("section", id="hadith")
if dua_section:
    category_wrap = soup.new_tag("div", id="dua-categories-wrap")
    category_wrap["class"] = ["dua-categories-wrap"]
    category_toggle = soup.new_tag("button", id="dua-categories-toggle", type="button")
    category_toggle["class"] = ["dua-panel-toggle"]
    category_toggle["aria-controls"] = "dua-categories-wrap"
    category_toggle["aria-expanded"] = "true"
    category_toggle.string = "إخفاء الأدعية"
    dua_section.append(category_toggle)
    for ident in ["ct", "duas"]:
        node = dua_section.find(id=ident)
        if node:
            category_wrap.append(node.extract())
    dua_section.append(category_wrap)
    for sec, button_id, label, panel_id in [
        (praised_section, "toggle-praised", "الأدعية المأثورة", "praised"),
        (hadith_section, "toggle-hadith", "الأحاديث المأثورة", "hadith"),
    ]:
        if sec:
            sec["hidden"] = True
            sec["class"] = list(dict.fromkeys((sec.get("class") or []) + ["dua-nested-section"]))
            toggle = soup.new_tag("button", id=button_id, type="button")
            toggle["class"] = ["dua-panel-toggle"]
            toggle["aria-controls"] = panel_id
            toggle["aria-expanded"] = "false"
            toggle.string = "إظهار " + label
            dua_section.append(toggle)
            dua_section.append(sec)
    if hadith_section:
        heading = hadith_section.find(id="had-h")
        if heading:
            heading.string = "الأحاديث المأثورة"

for ident in ["memories", "more", "mlb", "mp-dialog", "mp-admin", "mp-lb", "tasbeeh-total-card"]:
    node = soup.find(id=ident)
    if node:
        node.decompose()

for old_style in list(soup.find_all("style")):
    if old_style.get("id") in ["mp-posts-styles", "contact-footer-refinement"]:
        old_style.decompose()

for sc in list(soup.find_all("script")):
    src = sc.get("src", "")
    js = sc.string or sc.get_text()
    if "al_jallad_theme" in js and len(js) < 500:
        sc.decompose()
        continue
    if "mp-config.js" in src or "supabase" in src or "MP_CONFIG" in js or "mp-dialog" in js or "beforeinstallprompt" in js:
        sc.decompose()
        continue
    if len(js) > 40000:
        boundary = "}(),function(){"
        first = js.find(boundary)
        second = js.find(boundary, first + len(boundary)) if first >= 0 else -1
        if second >= 0:
            js = "!function(){" + js[second + len(boundary):]
            sc.clear()
            sc.append(js)
    elif "/api/tasbeeh" in js:
        sc.decompose()

# Remove the lifetime tasbeeh total card, including its decorative icon.
total_card = soup.find(id="tasbeeh-total-card")
if total_card:
    total_card.decompose()

# Keep the original reciter artwork in the Quran player instead of replacing it.
for wrap in soup.select(".reciter-img-wrap"):
    wrap["aria-hidden"] = "false"

for a in list(soup.select('nav a[href="#more"]')):
    a.decompose()

if soup.footer:
    footer = soup.new_tag("footer")
    footer["class"] = ["mamdouh-footer"]
    p = soup.new_tag("p")
    p.string = "اللهم اجعل هذا العمل صدقةً جاريةً ونورًا ورحمةً له."
    small = soup.new_tag("small")
    small.string = "نسألكم الدعاء لممدوح ولجميع موتى المسلمين."
    share = soup.new_tag("div")
    share["class"] = ["mamdouh-share"]
    wa = soup.new_tag("a", id="share-wa", href="#", target="_blank", rel="noopener noreferrer")
    wa.string = "مشاركة عبر واتساب"
    fb = soup.new_tag("a", id="share-fb", href="#", target="_blank", rel="noopener noreferrer")
    fb.string = "مشاركة عبر فيسبوك"
    copy = soup.new_tag("button", id="btn-copy-link", type="button")
    copy.string = "نسخ رابط الموقع"
    share.extend([wa, fb, copy])
    footer.extend([p, small, share])
    soup.footer.replace_with(footer)

for link in list(soup.find_all("link")):
    rel = link.get("rel") or []
    href = link.get("href", "")
    if "manifest" in rel or "apple-touch-icon" in rel or ("icon" in rel and "fonts.googleapis.com" not in href):
        link.decompose()

replacements = [
    ("محمد أحمد الجلاد وصلاح محمد الجلاد", "ممدوح"),
    ("محمد أحمد الجلاد", "ممدوح"),
    ("صلاح محمد الجلاد", "ممدوح"),
    ("لا تنسوهما من دعائكم", "لا تنسوه من دعائكم"),
    ("لا تنسوهما", "لا تنسوه"),
    ("ادعُ لهما الآن", "ادعُ له الآن"),
    ("اللهم ارحم محمد أحمد الجلاد وصلاح محمد الجلاد، واغفر لهما، واجعل قبريهما روضة من رياض الجنة", "اللهم ارحم ممدوح واغفر له واجعل قبره روضةً من رياض الجنة"),
    ("اللهم اغفر لمحمد أحمد الجلاد وصلاح محمد الجلاد بحق هذا الاسم العظيم.", "اللهم اغفر لممدوح وارحمه بحق هذا الاسم العظيم."),
    ("أدعية للمرحومين محمد أحمد الجلاد وصلاح محمد الجلاد", "أدعية للمرحوم ممدوح"),
    ("صدقة جارية على روح المرحومين محمد أحمد الجلاد وصلاح محمد الجلاد، نسألكم الدعاء لهما بالرحمة والمغفرة:", "صدقة جارية على روح ممدوح، نسألكم الدعاء له بالرحمة والمغفرة:"),
    ("انشر شيئًا للمتوفى", "شارك رابط الموقع"),
    ("ممدوح", "ممدوح عبد الهادي الاسمر"),
    ("اللهم اغفر لهما وارحمهما، وعافهما واعفُ عنهما، وأكرم نُزلهما، ووسّع مُدخلهما.", "اللهم اغفر له وارحمه، وعافه واعفُ عنه، وأكرم نُزله، ووسّع مُدخله."),
    ("اللهم اغفر لهما وارحمهما", "اللهم اغفر له وارحمه"),
    ("عافهما واعفُ عنهما", "عافه واعفُ عنه"),
    ("أكرم نُزلهما", "أكرم نُزله"),
    ("وسّع مُدخلهما", "وسّع مُدخله"),
    ("اللهم اغفر لهما، وارفع درجتهما في المهديين، وافسح لهما في قبريهما، ونوّر لهما فيهما.", "اللهم اغفر له، وارفع درجته في المهديين، وافسح له في قبره، ونوّر له فيه."),
    ("اللهم اغفر لهما وثبتهما عند السؤال، وارحمهما رحمة واسعة.", "اللهم اغفر له وثبته عند السؤال، وارحمه رحمة واسعة."),
    ("اللهم اغفر لهما وارحمهما، واعف عنهما، وارفع درجاتهما.", "اللهم اغفر له وارحمه، واعف عنه، وارفع درجته."),
    ("أدعية مأثورة — بصيغة المثنى", "أدعية للمرحوم ممدوح عبد الهادي الاسمر"),
    ("الصياغة معدّلة للمثنى لتناسب الدعاء للمرحومين.", "صياغة دعاء مخصصة لممدوح، وليست نقلًا حرفيًا للحديث."),
    ("صياغة معدّلة للمثنى، ولا تُنسب حرفيًا إلى الحديث.", "صياغة دعاء مخصصة لممدوح، ولا تُنسب حرفيًا للحديث."),
    ("صياغة من الأسرة، وليس نصًا منقولًا عن النبي ﷺ.", "دعاء عام لممدوح، وليس نصًا منقولًا عن النبي ﷺ."),
    ("المرحومين", "المرحوم"), ("للمرحومين", "للمرحوم"),
    ("المتوفّيين", "المتوفى"), ("المتوفين", "المتوفى"), ("للمتوفّيين", "للمتوفى"),
    ("الفقيدين", "الفقيد"), ("al_jallad", "mamdouh_memorial"),
    ("عَائِلَات الجَلَّاد", "ممدوح عبد الهادي الاسمر"),
]

theme_css = r"""
@font-face{font-family:Lemonadaa;src:url('fonts/Lemonadaa_Light.ttf') format('truetype');font-weight:300;font-display:swap}
@font-face{font-family:Lemonadaa;src:url('fonts/Lemonadaa_Regular.ttf') format('truetype');font-weight:400;font-display:swap}
@font-face{font-family:Lemonadaa;src:url('fonts/Lemonadaa_Medium.ttf') format('truetype');font-weight:500;font-display:swap}
@font-face{font-family:Lemonadaa;src:url('fonts/Lemonadaa_SemiBold.ttf') format('truetype');font-weight:600;font-display:swap}
:root,[data-theme=light]{
--bg-main:#F8F6F3;--bg-gradient:linear-gradient(180deg,#F8F6F3 0%,#F1EEE9 100%);
--text-main:#332F2A;--text-muted:#857E71;--text-heading:#332F2A;
--card-bg:#FFFFFF;--card-inner:#F8F6F3;--border-color:#CFCAC2;--border-subtle:rgba(178,171,160,.35);
--glass-bg:rgba(255,255,255,.78);--glass-border:rgba(178,171,160,.38);--bn-bg:rgba(248,246,243,.96);
--mem-bg:#F8F6F3;--mem-text:#332F2A;--mem-card-bg:#FFFFFF;--mem-card-text:#332F2A;
--input-bg:#FFFFFF;--pill-bg:#E6E3DD;--pill-active-bg:#332F2A;--pill-active-text:#F8F6F3;
--player-bg:#E6E3DD;--player-btn-bg:#FFFFFF;--dialog-box-bg:#FFFFFF;--dialog-backdrop:rgba(51,47,42,.72);
--c0:#F8F6F3;--c1:#E6E3DD;--c2:#CFCAC2;--c3:#B2ABA0;--c4:#857E71;--c5:#332F2A;
--box-shadow-card:0 8px 24px rgba(51,47,42,.08);--me-gold:#857E71;
--me-gold-soft:rgba(133,126,113,.42);--me-gold-faint:rgba(133,126,113,.18);color-scheme:light}
html{scroll-behavior:smooth;background:#F8F6F3}
body{font-family:Lemonadaa,system-ui,sans-serif!important;background:var(--bg-gradient)!important;color:var(--text-main)!important}
button,input,textarea,select{font-family:Lemonadaa,system-ui,sans-serif!important}
.mamdouh-intro{width:min(100% - 28px,760px);margin:22px auto 18px;padding:30px 18px 24px;text-align:center;background:rgba(255,255,255,.62);border:1px solid var(--border-color);border-radius:26px;box-shadow:0 10px 30px rgba(51,47,42,.07)}
.mamdouh-intro-inner{display:flex;flex-direction:column;align-items:center}
.mamdouh-photo{display:block;width:min(58vw,230px);height:270px;object-fit:cover;object-position:center 28%;border-radius:20px;border:5px solid #fff;box-shadow:0 12px 30px rgba(51,47,42,.15)}
.mamdouh-name{margin:18px 0 5px;color:#332F2A;font-size:clamp(1.7rem,5vw,2.3rem);font-weight:600;line-height:1.5}
.mamdouh-subtitle{margin:0;color:#857E71;font-size:clamp(.88rem,2.7vw,1rem);line-height:1.9}
.sec-card{background:var(--card-bg)!important;color:var(--text-main)!important;border-color:var(--border-color)!important;box-shadow:var(--box-shadow-card)!important}
.sec-title{color:var(--text-heading)!important}
.sec-card p,.sec-card .muted,.sec-card small{color:var(--text-muted)}
.bn{background:var(--bn-bg)!important;border-color:var(--border-color)!important;backdrop-filter:blur(18px)}
.bn a.active,.bn a[aria-current=page]{background:var(--pill-active-bg)!important;color:var(--pill-active-text)!important}
.quran-mark{width:64px;height:64px;border-radius:18px;display:grid;place-items:center;background:#E6E3DD;color:#585248;font-size:12px;text-align:center;padding:8px}
.mamdouh-footer{width:min(100% - 32px,700px);margin:26px auto 110px;padding:20px 14px;text-align:center;color:var(--text-muted);border-top:1px solid var(--border-color);line-height:2}
.mamdouh-footer p{margin:0 0 6px;color:var(--text-main)}.mamdouh-footer small{font-size:.82rem}
.mamdouh-share{display:flex;justify-content:center;gap:9px;flex-wrap:wrap;margin-top:14px}
.mamdouh-share a,.mamdouh-share button{display:inline-flex;align-items:center;justify-content:center;min-height:42px;padding:9px 14px;border:1px solid var(--border-color);border-radius:999px;background:#fff;color:var(--text-main);text-decoration:none;font-size:.82rem;cursor:pointer}
.v2-pray-btn,[data-theme=light] .v2-pray-btn{background:linear-gradient(135deg,#E6E3DD 0%,#CFCAC2 100%)!important;color:#332F2A!important;border:3px solid #B2ABA0!important;box-shadow:0 8px 22px rgba(51,47,42,.14)!important}
.v2-pray-btn svg{stroke:currentColor!important}
.v2-pray-btn:active{background:linear-gradient(135deg,#CFCAC2 0%,#B2ABA0 100%)!important}
@media(max-width:520px){.mamdouh-intro{margin-top:12px;padding:22px 14px 18px;border-radius:22px}.mamdouh-photo{width:min(62vw,205px);height:240px}.mamdouh-footer{margin-bottom:100px}}
"""
style = soup.new_tag("style", id="mamdouh-theme-overrides")
style.string = theme_css
soup.head.append(style)

theme_script = soup.new_tag("script", id="mamdouh-theme-script")
theme_script.string = r"""(()=>{const root=document.documentElement;root.setAttribute("data-theme","light");try{localStorage.removeItem("mamdouh_theme")}catch(e){}const meta=document.querySelector('meta[name="theme-color"]');if(meta)meta.content="#F8F6F3"})();"""
soup.body.append(theme_script)

visitor_script = soup.new_tag("script", id="mamdouh-visitor-placeholder")
visitor_script.string = r"""(()=>{const el=document.getElementById('mamdouh-visitor-count');if(!el)return;const key='mamdouh_demo_visits_v1';let count=0;try{count=Math.max(0,Number(localStorage.getItem(key))||0)}catch(e){}const render=()=>{el.textContent=count.toLocaleString('ar-EG')};render();window.setInterval(()=>{count+=1;render();try{localStorage.setItem(key,String(count))}catch(e){}},180000)})();"""
soup.body.append(visitor_script)

dua_script = soup.new_tag("script", id="mamdouh-dua-panels")
dua_script.string = r"""(()=>{const bind=(id,btnId,showText,hideText)=>{const panel=document.getElementById(id),btn=document.getElementById(btnId);if(!panel||!btn)return;btn.addEventListener('click',()=>{const show=panel.hidden;panel.hidden=!show;btn.setAttribute('aria-expanded',String(show));btn.textContent=(show?hideText:showText)})};bind('dua-categories-wrap','dua-categories-toggle','إظهار الأدعية','إخفاء الأدعية');bind('praised','toggle-praised','إظهار الأدعية المأثورة','إخفاء الأدعية المأثورة');bind('hadith','toggle-hadith','إظهار الأحاديث المأثورة','إخفاء الأحاديث المأثورة')})();"""
soup.body.append(dua_script)

final_html = str(soup)
for old, new in replacements:
    final_html = final_html.replace(old, new)


for bad in ["محمد أحمد الجلاد", "صلاح محمد الجلاد", "mp-dialog", "MP_CONFIG", "supabase", "al_jallad", "بصيغة المثنى", "صياغة معدّلة للمثنى"]:
    if bad in final_html:
        raise RuntimeError("Unremoved reference content: " + bad)
if not Path("img/photo.jpg").exists():
    raise RuntimeError("Missing Mamdouh portrait")
if not Path("fonts/Lemonadaa_Regular.ttf").exists():
    raise RuntimeError("Missing Mamdouh font")
# Replace the requested legacy color globally in the complete generated page.
final_html = re.sub(r"#cfcac2|#cecdcb|#cecdcc", "#6a5f53", final_html, flags=re.IGNORECASE)
if re.search(r"#cfcac2|#cecdcb|#cecdcc", final_html, flags=re.IGNORECASE):
    raise RuntimeError("Legacy color remains in generated page")
Path("index.html").write_text(final_html, encoding="utf-8")
print("Generated Mamdouh page:", len(final_html.encode("utf-8")), "bytes")
