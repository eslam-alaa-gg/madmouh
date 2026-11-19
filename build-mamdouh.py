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
theme_btn = soup.new_tag("button", id="theme-toggle", type="button")
theme_btn["aria-label"] = "التبديل بين الوضع الليلي والنهاري"
theme_btn["aria-pressed"] = "false"
theme_btn["class"] = ["mamdouh-theme-toggle"]
sun_svg = BeautifulSoup('<svg id="sun-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.65 17.65l1.42 1.42M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.65 6.35l1.42-1.42"></path></svg>', "html.parser").svg
moon_svg = BeautifulSoup('<svg id="moon-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.2 15.1A8.5 8.5 0 0 1 8.9 3.8 8.7 8.7 0 1 0 20.2 15.1Z"></path></svg>', "html.parser").svg
moon_svg["hidden"] = True
theme_btn.extend([sun_svg, moon_svg])
theme_label = soup.new_tag("span", id="theme-label")
theme_label.string = "ليلي"
theme_btn.append(theme_label)
toolbar.extend([brand, theme_btn])
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
    ("اللهم اغفر لهما وارحمهما، وعافهما واعفُ عنهما، وأكرم نُزلهما، ووسّع مُدخلهما.", "اللهم اغفر له وارحمه، وعافه واعفُ عنه، وأكرم نُزله، ووسّع مُدخله."),
    ("اللهم اغفر لهما وارحمهما", "اللهم اغفر له وارحمه"),
    ("عافهما واعفُ عنهما", "عافه واعفُ عنه"),
    ("أكرم نُزلهما", "أكرم نُزله"),
    ("وسّع مُدخلهما", "وسّع مُدخله"),
    ("قبريهما", "قبره"),
    ("المرحومين", "المرحوم"),
    ("للمرحومين", "للمرحوم"),
    ("المتوفّيين", "المتوفى"),
    ("المتوفين", "المتوفى"),
    ("للمتوفّيين", "للمتوفى"),
    ("الفقيدين", "الفقيد"),
    ("لهما", "له"),
    ("ارحمهما", "ارحمه"),
    ("عافهما", "عافه"),
    ("اعفُ عنهما", "اعفُ عنه"),
    ("نزلهما", "نزله"),
    ("مدخلهما", "مدخله"),
    ("عليهما", "عليه"),
    ("al_jallad", "mamdouh_memorial"),
    ("عَائِلَات الجَلَّاد", "ممدوح"),
]

theme_css = r"""
@font-face{font-family:Lemonadaa;src:url('fonts/Lemonadaa_Light.ttf') format('truetype');font-weight:300;font-display:swap}
@font-face{font-family:Lemonadaa;src:url('fonts/Lemonadaa_Regular.ttf') format('truetype');font-weight:400;font-display:swap}
@font-face{font-family:Lemonadaa;src:url('fonts/Lemonadaa_Medium.ttf') format('truetype');font-weight:500;font-display:swap}
@font-face{font-family:Lemonadaa;src:url('fonts/Lemonadaa_SemiBold.ttf') format('truetype');font-weight:600;font-display:swap}
:root,[data-theme=light],[data-theme=dark]{
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

theme_and_panels_css = r"""
:root,[data-theme=light]{--bg-main:#F8F6F3;--bg-gradient:linear-gradient(180deg,#F8F6F3 0%,#F1EEE9 100%);--text-main:#332F2A;--text-muted:#857E71;--text-heading:#332F2A;--card-bg:#FFFFFF;--card-inner:#F8F6F3;--border-color:#CFCAC2;--pill-bg:#E6E3DD;--pill-active-bg:#332F2A;--pill-active-text:#F8F6F3;--box-shadow-card:0 8px 24px rgba(51,47,42,.08);color-scheme:light}
[data-theme=dark]{--bg-main:#191714;--bg-gradient:linear-gradient(180deg,#191714 0%,#24211D 100%);--text-main:#F1EEE9;--text-muted:#B2ABA0;--text-heading:#F8F6F3;--card-bg:#29251F;--card-inner:#332F2A;--border-color:#585248;--pill-bg:#403A32;--pill-active-bg:#E6E3DD;--pill-active-text:#332F2A;--box-shadow-card:0 8px 24px rgba(0,0,0,.24);color-scheme:dark}
html{background:var(--bg-main)!important}
body{background:var(--bg-gradient)!important;color:var(--text-main)!important;transition:background .2s,color .2s}
.mamdouh-toolbar{direction:rtl;width:min(100% - 32px,760px);margin:12px auto 8px;display:flex;align-items:center;justify-content:space-between;min-height:54px}
#mamdouh-brand{display:flex;align-items:center;justify-content:center;width:78px;height:42px;overflow:hidden;border-radius:10px;background:#F8F6F3;border:1px solid var(--border-color)}
#mamdouh-brand img{width:100%;height:100%;object-fit:contain}
.mamdouh-theme-toggle{display:inline-flex;align-items:center;justify-content:center;gap:7px;min-width:44px;min-height:42px;padding:7px 12px;border-radius:999px;border:1px solid var(--border-color);background:var(--card-bg);color:var(--text-main);font:500 .82rem Lemonadaa,system-ui,sans-serif;cursor:pointer}
.mamdouh-theme-toggle svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.mamdouh-theme-toggle svg[hidden]{display:none}
.mamdouh-visitor-counter{width:max-content;max-width:calc(100% - 32px);margin:2px auto 12px;padding:8px 18px;display:flex;align-items:center;justify-content:center;gap:10px;border:1px solid var(--border-color);border-radius:999px;background:var(--glass-bg);color:var(--text-muted);box-shadow:var(--box-shadow-card);font-size:.9rem}
.mamdouh-visitor-counter strong{color:var(--text-heading);font-family:Inter,Arial,sans-serif;font-size:1.05rem;font-variant-numeric:tabular-nums}
.mamdouh-intro{background:var(--glass-bg)!important;border-color:var(--border-color)!important}
.mamdouh-name{color:var(--text-heading)!important}
.mamdouh-subtitle{color:var(--text-muted)!important}
.sec-card{background:var(--card-bg)!important;color:var(--text-main)!important;border-color:var(--border-color)!important;box-shadow:var(--box-shadow-card)!important}
.sec-title{color:var(--text-heading)!important}
.sec-card p,.sec-card .muted,.sec-card small{color:var(--text-muted)}
.mamdouh-footer{color:var(--text-muted)!important;border-color:var(--border-color)!important}
.mamdouh-footer p{color:var(--text-main)!important}
.mamdouh-share a,.mamdouh-share button{background:var(--card-bg)!important;color:var(--text-main)!important;border-color:var(--border-color)!important}
.dua-panel-toggle{display:flex;width:100%;min-height:48px;align-items:center;justify-content:center;margin:12px 0;padding:10px 16px;border:1px solid var(--border-color);border-radius:16px;background:var(--card-inner);color:var(--text-main);font:500 .92rem Lemonadaa,system-ui,sans-serif;cursor:pointer}
.dua-nested-section{margin-top:12px}
.dua-nested-section[hidden],#dua-categories-wrap[hidden]{display:none!important}
#dua{display:flex;flex-direction:column;gap:10px}
#dua .dua-nested-section{width:100%;box-sizing:border-box}
#dua .dua-nested-section .sec-title{margin-top:4px}
[data-theme=dark] .mamdouh-intro{background:rgba(41,37,31,.9)!important}
[data-theme=dark] .quran-mark{background:#403A32;color:#F1EEE9}
[data-theme=dark] .bn{background:rgba(25,23,20,.9)!important;border-color:#585248!important}
[data-theme=dark] .bn a{color:#B2ABA0!important}
[data-theme=dark] .bn a[aria-current=page]{background:#E6E3DD!important;color:#332F2A!important}
[data-theme=dark] .v2-pray-btn{background:linear-gradient(135deg,#403A32 0%,#332F2A 100%)!important;color:#F1EEE9!important;border-color:#857E71!important}

[data-theme=dark] .sec-card{
  background:#211E19!important;color:#F3EBDD!important;border-color:#51483B!important;
  box-shadow:0 10px 28px rgba(0,0,0,.3)!important
}
[data-theme=dark] .sec-card :is(h1,h2,h3,h4,h5,h6,.sec-title,.title,.heading,strong,b,label){
  color:#F6EBD8!important
}
[data-theme=dark] .sec-card :is(p,span,small,li,div,a,button,em){color:#E9DDC9}
[data-theme=dark] .sec-card :is(.muted,.subtitle,.description,.caption,.hint,.secondary){color:#C2B49D!important}
[data-theme=dark] .sec-card :is([class*="quran"],[class*="surah"],[class*="audio"],[class*="player"],[class*="reciter"],[class*="dua"],[class*="verse"],[class*="ayah"],[class*="track"],[class*="control"]){
  background-color:#302A22!important;color:#F3EBDD!important;border-color:#655744!important
}
[data-theme=dark] .sec-card :is(button,a,[role="button"]){
  background-color:#3A3228!important;color:#F6EBD8!important;border-color:#75634B!important
}
[data-theme=dark] .sec-card :is(svg,i){color:#E8D7B8!important;stroke:currentColor}
[data-theme=dark] .sec-card :is(input,select,textarea){background:#302A22!important;color:#F6EBD8!important;border-color:#75634B!important}
[data-theme=dark] .sec-card :is(input,select,textarea)::placeholder{color:#BDAE96!important}
[data-theme=dark] .sec-card :is(.progress,.progress-bar,.audio-progress,[class*="progress"]){background:#51483B!important}
[data-theme=dark] .sec-card :is(.progress,[class*="progress"]) :is(i,span){background:#C7A979!important}


/* Dark palette for the standalone dua and tasbeeh views */
[data-theme=dark] body,
[data-theme=dark] main{color:#F3EBDD!important}
[data-theme=dark] .glass,
[data-theme=dark] .glass.dua,
[data-theme=dark] .glass.tas,
[data-theme=dark] .glass.err{
  background:linear-gradient(145deg,#29241D 0%,#211D18 100%)!important;
  color:#F3EBDD!important;border:1px solid #514637!important;
  box-shadow:0 18px 42px rgba(0,0,0,.34)!important
}
[data-theme=dark] .dua-text,
[data-theme=dark] .dhikr,
[data-theme=dark] .count,
[data-theme=dark] .glass :is(h1,h2,h3,b,strong){color:#F6EBD8!important}
[data-theme=dark] .glass .muted,
[data-theme=dark] .glass .note,
[data-theme=dark] .glass .dua-foot,
[data-theme=dark] .glass p:not(.dua-text):not(.dhikr):not(.note){color:#CBBDA6!important}
[data-theme=dark] .dua-foot{border-color:#514637!important}
[data-theme=dark] .glass .icon,
[data-theme=dark] .glass .btn:not(.dark),
[data-theme=dark] .chip,
[data-theme=dark] .custom input{
  background:#383025!important;color:#F3EBDD!important;
  border:1px solid #6A5943!important
}
[data-theme=dark] .btn.dark,
[data-theme=dark] .chip[aria-pressed=true],
[data-theme=dark] .nav a[aria-current=page]{
  background:#C7AD82!important;border-color:#C7AD82!important;color:#211D18!important
}
[data-theme=dark] .tap{
  background:radial-gradient(circle at 35% 28%,#786447,#3B3022 72%)!important;
  color:#F6EBD8!important;box-shadow:inset 0 2px 0 rgba(255,255,255,.12),0 22px 42px rgba(0,0,0,.42)!important
}
[data-theme=dark] .bar{background:#494033!important}
[data-theme=dark] .bar i{background:#C7AD82!important}
[data-theme=dark] .nav{
  background:rgba(34,29,23,.94)!important;border-color:#514637!important
}
[data-theme=dark] .nav a{color:#CBBDA6!important}
[data-theme=dark] dialog{
  background:#211D18!important;color:#F3EBDD!important;border:1px solid #514637!important
}
[data-theme=dark] .opt{
  background:#302920!important;color:#F3EBDD!important;border-color:#514637!important
}
[data-theme=dark] .opt small{color:#CBBDA6!important}
[data-theme=dark] .opt[aria-current=true]{background:#C7AD82!important;color:#211D18!important;border-color:#C7AD82!important}
[data-theme=dark] .opt[aria-current=true] small{color:#33291D!important}
[data-theme=dark] .grp{color:#CBBDA6!important}
[data-theme=dark] .custom input::placeholder{color:#B8A98F!important}


/* Explicit dark styling for the actual dua and tasbeeh view IDs */
[data-theme="dark"] #duas,
[data-theme="dark"] #tasbeeh{color:#F4EBDD!important}
[data-theme="dark"] #duas > .glass,
[data-theme="dark"] #tasbeeh > .glass,
[data-theme="dark"] #duas .glass.dua,
[data-theme="dark"] #tasbeeh .glass.tas,
[data-theme="dark"] #duas .glass.err{
  background:#201C17!important;
  background-image:linear-gradient(145deg,#29231B 0%,#1D1A16 100%)!important;
  color:#F4EBDD!important;
  border:1px solid #66553E!important;
  box-shadow:0 14px 36px rgba(0,0,0,.48)!important;
  -webkit-backdrop-filter:none!important;backdrop-filter:none!important
}
[data-theme="dark"] #duas .dua-text,
[data-theme="dark"] #tasbeeh .dhikr,
[data-theme="dark"] #tasbeeh .count{color:#FFF2DA!important}
[data-theme="dark"] #duas #d-src,
[data-theme="dark"] #duas #d-idx,
[data-theme="dark"] #tasbeeh #t-combo,
[data-theme="dark"] #tasbeeh #t-of,
[data-theme="dark"] #tasbeeh #t-note,
[data-theme="dark"] #duas .muted,
[data-theme="dark"] #tasbeeh .muted{color:#D1C0A5!important}
[data-theme="dark"] #duas .dua-foot{border-top-color:#514432!important}
[data-theme="dark"] #duas .icon,
[data-theme="dark"] #duas .btn:not(.dark),
[data-theme="dark"] #tasbeeh .btn:not(.dark),
[data-theme="dark"] #tasbeeh .chip,
[data-theme="dark"] #tasbeeh .custom input{
  background:#332B21!important;color:#FFF0D6!important;
  border:1px solid #786344!important
}
[data-theme="dark"] #duas .btn.dark,
[data-theme="dark"] #tasbeeh .btn.dark,
[data-theme="dark"] #tasbeeh .chip[aria-pressed="true"]{
  background:#B99B6C!important;border-color:#B99B6C!important;color:#1D1913!important
}
[data-theme="dark"] #tasbeeh .tap{
  background:radial-gradient(circle at 35% 28%,#806847 0%,#493722 72%)!important;
  color:#FFF1D8!important;border:1px solid #A88A5E!important;
  box-shadow:inset 0 2px 0 rgba(255,255,255,.12),0 22px 42px rgba(0,0,0,.55)!important
}
[data-theme="dark"] #tasbeeh .bar{background:#514637!important}
[data-theme="dark"] #tasbeeh .bar i{background:#C7A979!important}
[data-theme="dark"] #tasbeeh .chip{color:#F4EBDD!important}
[data-theme="dark"] #tasbeeh .custom input::placeholder{color:#C7B698!important}
[data-theme="dark"] #tasbeeh .center .btn,
[data-theme="dark"] #duas .center .btn{background:#332B21!important;color:#FFF0D6!important;border-color:#786344!important}
[data-theme="dark"] #tasbeeh .center .btn.dark,
[data-theme="dark"] #duas .center .btn.dark{background:#B99B6C!important;color:#1D1913!important}


/* Darken every individual dua tile, not only the outer section */
html[data-theme="dark"] #dua,
html[data-theme="dark"] #praised,
html[data-theme="dark"] #hadith,
html[data-theme="dark"] #dua-categories-wrap{
  background:transparent!important;color:#F4EBDD!important
}
html[data-theme="dark"] #dua :is(.sec-card,.card,.dua-card,.dua-item,[class*="dua-card"],[class*="dua-item"],[class*="prayer-card"],[class*="category-card"]),
html[data-theme="dark"] #praised :is(.sec-card,.card,.dua-card,.dua-item,[class*="dua-card"],[class*="dua-item"]),
html[data-theme="dark"] #hadith :is(.sec-card,.card,.dua-card,.dua-item,[class*="dua-card"],[class*="dua-item"]){
  background:#211E19!important;
  background-color:#211E19!important;
  background-image:linear-gradient(145deg,#29231B 0%,#1D1A16 100%)!important;
  color:#F4EBDD!important;border-color:#66553E!important;
  box-shadow:0 10px 28px rgba(0,0,0,.42)!important
}
html[data-theme="dark"] #dua :is(.sec-card,.card,.dua-card,.dua-item,[class*="dua-card"],[class*="dua-item"],[class*="prayer-card"],[class*="category-card"]) :is(p,span,small,li,strong,b,h1,h2,h3,h4),
html[data-theme="dark"] #praised :is(.sec-card,.card,.dua-card,.dua-item,[class*="dua-card"],[class*="dua-item"]) :is(p,span,small,li,strong,b,h1,h2,h3,h4),
html[data-theme="dark"] #hadith :is(.sec-card,.card,.dua-card,.dua-item,[class*="dua-card"],[class*="dua-item"]) :is(p,span,small,li,strong,b,h1,h2,h3,h4){
  color:#F3EBDD!important
}
html[data-theme="dark"] #dua :is(.dua-panel-toggle,[class*="toggle"]),
html[data-theme="dark"] #praised :is(.dua-panel-toggle,[class*="toggle"]),
html[data-theme="dark"] #hadith :is(.dua-panel-toggle,[class*="toggle"]){
  background:#302920!important;color:#F6EBD8!important;border-color:#66553E!important
}

@media(max-width:520px){.mamdouh-toolbar{margin-top:8px}.mamdouh-visitor-counter{margin-bottom:8px}}

/* Match the requested dark palette on the individual dua cards only. */
html[data-theme="dark"] #dua :is(.sec-card,.card,.dua-card,.dua-item,[class*="dua-card"],[class*="dua-item"],[class*="prayer-card"],[class*="category-card"]),
html[data-theme="dark"] #praised :is(.sec-card,.card,.dua-card,.dua-item,[class*="dua-card"],[class*="dua-item"]),
html[data-theme="dark"] #hadith :is(.sec-card,.card,.dua-card,.dua-item,[class*="dua-card"],[class*="dua-item"]){
  background:#6a5f53!important;
  background-color:#6a5f53!important;
  background-image:none!important;
}
"""
theme_style = soup.new_tag("style", id="mamdouh-theme-panels")
theme_style.string = theme_and_panels_css
soup.head.append(theme_style)

theme_script = soup.new_tag("script", id="mamdouh-theme-script")
theme_script.string = r"""(()=>{const root=document.documentElement,btn=document.getElementById('theme-toggle'),sun=document.getElementById('sun-icon'),moon=document.getElementById('moon-icon'),label=document.getElementById('theme-label');if(!btn)return;let saved='light';try{saved=localStorage.getItem('mamdouh_theme')||'light'}catch(e){}const apply=t=>{root.setAttribute('data-theme',t);sun.hidden=t==='dark';moon.hidden=t!=='dark';label.textContent=t==='dark'?'نهاري':'ليلي';btn.setAttribute('aria-pressed',String(t==='dark'));const meta=document.querySelector('meta[name="theme-color"]');if(meta)meta.content=t==='dark'?'#191714':'#F8F6F3'};apply(saved);btn.addEventListener('click',()=>{const t=root.getAttribute('data-theme')==='dark'?'light':'dark';apply(t);try{localStorage.setItem('mamdouh_theme',t)}catch(e){}})})();"""
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
extra = [
    ("اللهم ارحم محمد أحمد الجلاد وصلاح محمد الجلاد، واغفر لهما، واجعل قبريهما روضة من رياض الجنة", "اللهم ارحم ممدوح واغفر له واجعل قبره روضةً من رياض الجنة"),
    ("اللهم اغفر لمحمد أحمد الجلاد وصلاح محمد الجلاد بحق هذا الاسم العظيم.", "اللهم اغفر لممدوح وارحمه بحق هذا الاسم العظيم."),
    ("أدعية للمرحومين محمد أحمد الجلاد وصلاح محمد الجلاد", "أدعية للمرحوم ممدوح"),
    ("صدقة جارية على روح المرحومين محمد أحمد الجلاد وصلاح محمد الجلاد، نسألكم الدعاء لهما بالرحمة والمغفرة:", "صدقة جارية على روح ممدوح، نسألكم الدعاء له بالرحمة والمغفرة:"),
    ("انشر شيئًا للمتوفى", "شارك رابط الموقع"),
    ("assets/audio/quran/surah/surah-ya-sin.mp3", "https://sadakah-58j1.vercel.app/surah-ya-sin.mp3"),
]
for old, new in extra:
    final_html = final_html.replace(old, new)

# Use the full memorial name consistently in every visible page location and metadata.
final_html = final_html.replace("ممدوح", "ممدوح عبد الهادي الاسمر")
for old, new in [
    ("وارحمهما", "وارحمه"), ("ارحمهما", "ارحمه"), ("وعافهما", "وعافه"),
    ("عنهما", "عنه"), ("نُزلهما", "نُزله"), ("مُدخلهما", "مُدخله"),
    ("درجتهما", "درجته"), ("قبريهما", "قبره"), ("فيهما", "فيه"),
    ("وثبتهما", "وثبته"), ("درجاتهما", "درجاته"), ("أبدلهما", "أبدله"),
    ("دارهما", "داره"), ("أهلهما", "أهله"), ("وأدخلهما", "وأدخله"),
    ("وأعذهما", "وأعذه"), ("وحشتهما", "وحشته"), ("وقرارهما", "وقراره"),
    ("درجتيهما", "درجته"), ("واجمعهما", "واجمعه"), ("أسكنهما", "أسكنه"),
    ("وارزقهما", "وارزقه"), ("ذكراهما", "ذكراه"), ("وثبّتهما", "وثبّته"),
    ("سيئاتهما", "سيئاته"), ("اجعلهما", "اجعله"), ("ومتّعهما", "ومتّعه"),
    ("تصلهما", "تصله"), ("لهما", "له"), ("عليهما", "عليه")
]:
    final_html = final_html.replace(old, new)

for bad in ["محمد أحمد الجلاد", "صلاح محمد الجلاد", "لهما", "المرحومين", "قبريهما", "انشر تؤجر", "انشر شيئًا للمتوفى", "mp-dialog", "MP_CONFIG", "supabase", "al_jallad", "إنشاء صدقه"]:
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
