#!/usr/bin/env python3
"""Builds services.html and comfort-club.html and syncs header/footer links on all four pages.
Run from the project root:  python3 tools/build_inner.py
Header, footer and icon sprite are taken from about.html so all pages stay identical."""
import re, io
BOOK='https://book.housecallpro.com/book/Cosmos-Heating--Air-Conditioning/5dd6087d1c134f25b5e4cfb80da8b594?v2=true'
LINKS=[('Services','services.html'),('Cosmo’s Comfort Club','comfort-club.html'),
       ('Repair Services','services.html#repair'),('Installation Services','services.html#installation'),
       ('Maintenance Services','services.html#maintenance'),('Indoor Air Quality','services.html#air-quality'),
       ('Air Duct Cleaning','services.html#air-quality')]
def fix_links(h):
    for text,href in LINKS:
        h=re.sub(r'<a href="[^"]*"((?: class="[^"]*")?(?: aria-current="page")?)>'+re.escape(text)+'</a>',
                 lambda m:'<a href="%s"%s>%s</a>'%(href,m.group(1),text),h)
    return h
def set_active(h,label):
    h=h.replace(' class="is-active" aria-current="page"','').replace(' class="is-active"','')
    return re.sub(r'(<a href="[^"]*")>'+re.escape(label)+'</a>',r'\1 class="is-active" aria-current="page">'+label+'</a>',h,count=1)

# ---- sync existing pages (links only) ----
for f in ('index.html','about.html'):
    s=open(f).read(); s=fix_links(s)
    if f=='about.html': s=set_active(s,'About')
    open(f,'w').write(s)

about=open('about.html').read()
def cut(a,b,src=about): i=src.index(a); return src[i:src.index(b,i)]
SPRITE=cut('<svg width="0"','<a class="skip"')
HEADER=cut('<a class="skip"','<main')
FOOTER=cut('<!-- FOOTER -->','<script src="script.js"')
EXTRA='''<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <symbol id="s-chat" viewBox="0 0 48 48"><path d="M7 9h34v22H23l-9 8v-8H7z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M15 18h18M15 24h11" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></symbol>
  <symbol id="s-cal" viewBox="0 0 48 48"><rect x="7" y="11" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M7 20h34M16 6v9M32 6v9" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="m18 30 4 4 8-8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="s-search" viewBox="0 0 48 48"><circle cx="21" cy="21" r="12" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="m30 30 11 11" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></symbol>
  <symbol id="s-alert" viewBox="0 0 48 48"><path d="M24 7 43 40H5z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M24 19v10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="24" cy="34" r="1.4" fill="currentColor"/></symbol>
  <symbol id="s-snow" viewBox="0 0 48 48"><path d="M24 6v36M8.400 15l31.200 18M8.400 33l31.200-18" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="24" cy="24" r="4" fill="none" stroke="currentColor" stroke-width="1.6"/></symbol>
</svg>
'''
SPRITE=SPRITE+EXTRA

def icon(i,cls): return '<svg class="%s" aria-hidden="true"><use href="#%s"/></svg>'%(cls,i)
ARROW='<svg class="ic"><use href="#i-arrow"/></svg>'
def head(title,desc,url,ogtitle,ld):
    return f'''<!DOCTYPE html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.replace('no-js','js')</script>
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://www.cosmosaclv.com/{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#06303d">
<meta name="geo.region" content="US-NV"><meta name="geo.placename" content="Las Vegas">
<meta property="og:type" content="website"><meta property="og:site_name" content="Cosmo's Heating and Air Conditioning">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://www.cosmosaclv.com/{url}">
<meta name="twitter:card" content="summary_large_image">
<!-- TODO: add <meta property="og:image"> (1200x630) once a final photo is chosen -->
<link rel="icon" href="assets/images/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Poppins:wght@400;500;600&display=swap">
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="css/about.css">
<link rel="stylesheet" href="css/pages.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body class="about-body">
<div class="a-curtain" aria-hidden="true"></div>

'''
TAIL='''
<script src="script.js" defer></script>
<script src="js/about.js" defer></script>
<script src="js/pages.js" defer></script>
</body>
</html>
'''
import json
def faq_html(items):
    return '<div class="faq">\n'+'\n'.join(f'''  <details data-a{' style="--d:%.2fs"'%(i*.06) if i else ''}><summary>{q}</summary><div class="faq__a"><p>{a}</p></div></details>''' for i,(q,a) in enumerate(items))+'\n</div>'
def faq_ld(items):
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":re.sub('<[^>]+>','',q).replace('&rsquo;','’').replace('&amp;','&'),"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a).replace('&rsquo;','’').replace('&amp;','&')}} for q,a in items]}
def crumbs(name,url): return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.cosmosaclv.com/"},{"@type":"ListItem","position":2,"name":name,"item":"https://www.cosmosaclv.com/"+url}]}
BUSINESS={"@type":["HVACBusiness","LocalBusiness"],"@id":"https://www.cosmosaclv.com/#business","name":"Cosmo's Heating and Air Conditioning","alternateName":"Cosmos HVAC","url":"https://www.cosmosaclv.com/","telephone":"+1-702-960-5555","email":"service@cosmosaclv.com","address":{"@type":"PostalAddress","streetAddress":"10161 W Park Run Dr #150","addressLocality":"Las Vegas","addressRegion":"NV","postalCode":"89145","addressCountry":"US"},"areaServed":["Las Vegas, NV","Henderson, NV","North Las Vegas, NV"]}

# =========================== SERVICES ===========================
SFAQ=[
 ("How often should I schedule HVAC maintenance?","Most manufacturers recommend having heating and cooling equipment inspected at least once a year, and many homeowners in the Las Vegas heat schedule a check before summer. Cosmo’s Comfort Club is built around year-round maintenance, so ask our team which schedule suits your system."),
 ("When should I repair or replace my AC system?","It depends on the age of the equipment, how often it needs repair and how well it keeps you comfortable. After a diagnostic, our technicians explain your options plainly so you can decide what makes sense for your property."),
 ("What are common signs that my AC needs repair?","Weak airflow, rooms that won’t cool, unusual noises, odors, short cycling or a sudden rise in energy bills are all reasons to have the system checked. If your AC stops cooling, call our team."),
 ("How long does HVAC installation take?","The timeline depends on the type of system, the size of the property and the work involved. We’ll walk through the scope with you and confirm the schedule before work begins."),
 ("Does Cosmos offer residential and commercial HVAC services?","Yes. Cosmo’s Heating &amp; Air Conditioning serves both homeowners and businesses across Las Vegas, Henderson and North Las Vegas."),
]
def services():
    ld=json.dumps({"@context":"https://schema.org","@graph":[
        {"@type":"WebPage","@id":"https://www.cosmosaclv.com/services.html#page","url":"https://www.cosmosaclv.com/services.html","name":"HVAC Services in Las Vegas","isPartOf":{"@id":"https://www.cosmosaclv.com/#business"}},
        crumbs("Services","services.html"),BUSINESS,faq_ld(SFAQ)]},ensure_ascii=False)
    h=head("HVAC Services in Las Vegas | AC Repair, Installation &amp; Maintenance | Cosmo’s",
      "AC repair, HVAC installation, preventative maintenance and indoor air quality for Las Vegas, Henderson and North Las Vegas homes and businesses. Licensed #0095036. Schedule a service today.",
      "services.html","HVAC Services in Las Vegas | Cosmo’s Heating &amp; Air Conditioning",ld)
    h+=SPRITE+HEADER+f'''<main id="main" class="about-page">

<!-- ===== 1 · HERO ===== -->
<section class="s-hero" aria-labelledby="s-hero-title">
  <div class="wrap s-hero__grid">
    <div>
      <p class="a-eyebrow" data-a>Our HVAC Services</p>
      <h1 id="s-hero-title" class="a-display" data-split>Complete Comfort Solutions <em>for Every Space.</em></h1>
      <p class="a-lead" data-a style="--d:.4s">From reliable air conditioning repairs to professional HVAC installations and routine maintenance, Cosmos delivers dependable comfort solutions for Las Vegas homes and businesses.</p>
      <div class="s-btns" data-a style="--d:.55s">
        <a class="btn btn--caps" href="{BOOK}" target="_blank" rel="noopener">Schedule a Service {ARROW}</a>
        <a class="btn btn--caps btn--ghost" href="tel:+17029605555">{icon('i-phone','ic')}Call Our Team</a>
      </div>
    </div>
    <div class="s-hero__media">
      <figure class="s-photo s-hero__photo a-img"><img src="assets/services/hero.jpg" alt="Cosmo’s HVAC technician in a red uniform servicing an outdoor air conditioning condenser unit" width="900" height="900" decoding="async"></figure>
      <p class="s-hero__chip" data-a style="--d:.5s">{icon('i-badge','ic')}<span>Licensed Contractor<br>#0095036</span></p>
    </div>
  </div>
  <svg class="a-wave" viewBox="0 0 1440 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0 40c240 30 480 30 720 8s480-30 720 0v12H0z" fill="#fff"/></svg>
</section>

<!-- ===== 2 · SERVICE CARDS ===== -->
<section class="s-sec" aria-labelledby="s-cards-title">
  <div class="wrap">
    <header class="s-head s-head--center">
      <p class="a-label" data-a><span>01</span>What we do</p>
      <h2 id="s-cards-title" class="a-h2" data-split>Complete <em>HVAC Services</em></h2>
      <p class="a-lead" data-a>Trusted HVAC service and installation by Man’s Most Reliable — from repair to maintenance.</p>
    </header>
    <ul class="s-cards">
      <li class="s-card" data-a>
        <figure class="s-card__media"><img src="assets/services/card-repair.jpg" alt="Technician repairing a rooftop air conditioning unit in Las Vegas" width="259" height="300" loading="lazy" decoding="async"></figure>
        <div class="s-card__body"><p class="s-card__tag">Repair</p><h3>AC Repair</h3><p>Fast, dependable air conditioning repair to help restore comfort when your cooling system isn’t working properly.</p><a class="s-card__more" href="#repair">Learn More {ARROW}</a></div>
      </li>
      <li class="s-card" data-a style="--d:.08s">
        <figure class="s-card__media"><img src="assets/services/card-install.jpg" alt="Commercial rooftop HVAC unit being lowered into position during installation" width="322" height="224" loading="lazy" decoding="async"></figure>
        <div class="s-card__body"><p class="s-card__tag">Installation</p><h3>HVAC Installation</h3><p>Professional heating and cooling system installation designed around your property, comfort requirements and efficiency goals.</p><a class="s-card__more" href="#installation">Learn More {ARROW}</a></div>
      </li>
      <li class="s-card" data-a style="--d:.16s">
        <figure class="s-card__media"><img src="assets/services/card-maintenance.jpg" alt="Residential air conditioner condenser beside a desert-landscaped Las Vegas home" width="402" height="402" loading="lazy" decoding="async"></figure>
        <div class="s-card__body"><p class="s-card__tag">Maintenance</p><h3>HVAC Maintenance</h3><p>Routine inspections and preventative maintenance to help keep your HVAC equipment operating reliably throughout the year.</p><a class="s-card__more" href="#maintenance">Learn More {ARROW}</a></div>
      </li>
      <li class="s-card" data-a style="--d:.24s">
        <figure class="s-card__media"><img src="assets/services/card-air.jpg" alt="Technician’s gloved hand replacing an air filter inside an HVAC unit" width="323" height="224" loading="lazy" decoding="async"></figure>
        <div class="s-card__body"><p class="s-card__tag">Air Quality</p><h3>Indoor Air Quality &amp; Duct Cleaning</h3><p>Solutions to help improve indoor air quality, support better airflow and maintain a cleaner, healthier indoor environment.</p><a class="s-card__more" href="#air-quality">Learn More {ARROW}</a></div>
      </li>
    </ul>
  </div>
</section>

<!-- ===== 3 · AC REPAIR ===== -->
<section class="s-sec s-sec--cream s-split" id="repair" aria-labelledby="repair-title">
  <div class="wrap s-split__grid">
    <div class="s-split__media"><figure class="s-photo a-img"><img src="assets/services/repair.jpg" alt="Cosmo’s technician diagnosing an outdoor commercial HVAC unit on a Las Vegas rooftop" width="349" height="461" loading="lazy" decoding="async"></figure>
      <figure class="s-photo s-photo--inset a-img" style="--d:.2s"><img src="assets/services/repair-detail.jpg" alt="Close-up of a technician’s gloved hands checking an air conditioner’s components" width="680" height="480" loading="lazy" decoding="async"></figure></div>
    <div class="s-split__text">
      <p class="a-label" data-a><span>02</span>AC Repair</p>
      <h2 id="repair-title" class="a-h2" data-split>When Your Comfort Needs Attention, <em>We’re Here.</em></h2>
      <p class="a-lead" data-a>When your cooling stops working, you need honest answers and a fast, dependable fix. Our technicians find the real cause before recommending a repair.</p>
      <ul class="s-list" data-a><li>AC system diagnostics</li><li>Cooling performance issues</li><li>Airflow problems</li><li>Unusual noises and system issues</li><li>Clear repair recommendations in plain English</li></ul>
      <a class="btn btn--caps" data-a href="{BOOK}" target="_blank" rel="noopener">Schedule AC Repair {ARROW}</a>
    </div>
  </div>
</section>

<!-- ===== 4 · INSTALLATION ===== -->
<section class="s-sec s-split s-split--rev" id="installation" aria-labelledby="install-title">
  <div class="wrap s-split__grid">
    <div class="s-split__media"><figure class="s-photo a-img"><img src="assets/services/install.jpg" alt="Rooftop HVAC unit lifted by crane during a commercial installation in Las Vegas" width="348" height="461" loading="lazy" decoding="async"></figure></div>
    <div class="s-split__text">
      <p class="a-label" data-a><span>03</span>HVAC Installation</p>
      <h2 id="install-title" class="a-h2" data-split>The Right System. <em>Installed the Right Way.</em></h2>
      <p class="a-lead" data-a>A well-chosen system that’s installed carefully is the foundation of lasting comfort — for a Las Vegas home or a commercial property.</p>
      <ul class="s-list" data-a><li>Residential HVAC installation</li><li>Commercial HVAC installation</li><li>System replacement</li><li>Equipment selection guidance</li><li>Professional installation and testing</li></ul>
      <a class="btn btn--caps" data-a href="index.html#contact">Request an Estimate {ARROW}</a>
    </div>
  </div>
</section>

<!-- ===== 5 · MAINTENANCE ===== -->
<section class="s-sec s-sec--mint s-split" id="maintenance" aria-labelledby="maint-title">
  <div class="wrap s-split__grid">
    <div class="s-split__media"><figure class="s-photo a-img"><img src="assets/services/maintenance.jpg" alt="Cosmo’s technician on a ladder inspecting ceiling-mounted HVAC equipment" width="326" height="224" loading="lazy" decoding="async"></figure></div>
    <div class="s-split__text">
      <p class="a-label" data-a><span>04</span>Preventative Maintenance</p>
      <h2 id="maint-title" class="a-h2" data-split>Protect Your Comfort <em>Before Problems Start.</em></h2>
      <p class="a-lead" data-a>Regular maintenance helps equipment run reliably, helps catch small issues early and keeps your system ready for Las Vegas’ extreme seasons.</p>
      <ul class="s-list" data-a><li>System inspections</li><li>Filter and airflow checks</li><li>Equipment performance checks</li><li>Preventative recommendations</li><li>Seasonal maintenance</li></ul>
      <a class="btn btn--caps" data-a href="comfort-club.html">Explore the Comfort Club {ARROW}</a>
    </div>
  </div>
</section>

<!-- ===== 6 · INDOOR AIR QUALITY ===== -->
<section class="s-sec s-split s-split--rev s-split--wide" id="air-quality" aria-labelledby="air-title">
  <div class="wrap s-split__grid">
    <div class="s-split__media"><figure class="s-photo a-img"><img src="assets/services/air-quality.jpg" alt="Exposed insulated HVAC ductwork running through a commercial building" width="349" height="330" loading="lazy" decoding="async"></figure></div>
    <div class="s-split__text">
      <p class="a-label" data-a><span>05</span>Indoor Air Quality</p>
      <h2 id="air-title" class="a-h2" data-split>Breathe Easier. <em>Feel Better at Home.</em></h2>
      <p class="a-lead" data-a>Clean, well-balanced airflow makes a home or workspace more comfortable. We help you find practical ways to improve the air you breathe.</p>
      <ul class="s-list" data-a><li>Indoor air quality solutions</li><li>Duct inspection and cleaning, where offered</li><li>Airflow improvements</li><li>Filter and ventilation recommendations</li></ul>
      <a class="btn btn--caps" data-a href="tel:+17029605555">{icon('i-phone','ic')}Ask About Air Quality</a>
    </div>
  </div>
</section>

<!-- ===== 7 · WHY COSMOS (dark) ===== -->
<section class="s-why" aria-labelledby="why-title">
  <div class="wrap">
    <header class="s-head">
      <p class="a-label a-label--light" data-a><span>06</span>Why choose Cosmos</p>
      <h2 id="why-title" class="a-h2" data-split>A Higher Standard <em>of HVAC Service.</em></h2>
    </header>
    <ul class="s-why__grid">
      <li class="s-why__item" data-a>{icon('a-gauge','s-why__ic')}<h3>Experienced Professionals</h3><p>Certified, multi-service technicians with hands-on HVAC experience.</p></li>
      <li class="s-why__item" data-a style="--d:.1s">{icon('s-chat','s-why__ic')}<h3>Honest Recommendations</h3><p>Plain-English explanations and transparent pricing — never pressure.</p></li>
      <li class="s-why__item" data-a style="--d:.2s">{icon('a-wrench','s-why__ic')}<h3>Quality Workmanship</h3><p>Careful, clean work backed by the Cosmo’s Comfort Guarantee™.</p></li>
      <li class="s-why__item" data-a style="--d:.3s">{icon('a-heart','s-why__ic')}<h3>Customer-Focused Service</h3><p>A locally owned team that treats your home or business like its own.</p></li>
    </ul>
  </div>
</section>

<!-- ===== 8 · SERVICE PROCESS ===== -->
<section class="s-sec" aria-labelledby="proc-title">
  <div class="wrap">
    <header class="s-head">
      <p class="a-label" data-a><span>07</span>Our service process</p>
      <h2 id="proc-title" class="a-h2" data-split>Simple From the <em>First Call.</em></h2>
    </header>
    <ol class="a-steps" data-progress>
      <li class="a-step" data-a><span class="a-step__no" aria-hidden="true">01</span><h3>Tell Us What You Need</h3><p>Call or book online and tell us about your system and your comfort concern.</p></li>
      <li class="a-step" data-a style="--d:.12s"><span class="a-step__no" aria-hidden="true">02</span><h3>Schedule Your Appointment</h3><p>Choose a time that works for your home or business.</p></li>
      <li class="a-step" data-a style="--d:.24s"><span class="a-step__no" aria-hidden="true">03</span><h3>Get Professional Service</h3><p>Our technician diagnoses, explains your options and completes the work with care.</p></li>
      <li class="a-step" data-a style="--d:.36s"><span class="a-step__no" aria-hidden="true">04</span><h3>Enjoy Reliable Comfort</h3><p>Relax in a comfortable space with a team that stands behind its work.</p></li>
    </ol>
  </div>
</section>

<!-- ===== 9 · SERVICE AREA ===== -->
<section class="s-sec s-sec--sky s-area" aria-labelledby="area-title">
  <div class="wrap s-area__grid">
    <div>
      <p class="a-label" data-a><span>08</span>Service area</p>
      <h2 id="area-title" class="a-h2" data-split>Proudly Serving <em>the Las Vegas Valley.</em></h2>
      <ul class="s-area__chips" data-a>
        <li>{icon('i-pin','ic')}Las Vegas</li><li>{icon('i-pin','ic')}Henderson</li><li>{icon('i-pin','ic')}North Las Vegas</li>
      </ul>
      <p class="s-area__note" data-a>Looking for service outside these cities? Call <a class="a-link-dark" href="tel:+17029605555">+1 (702) 960-5555</a> and we’ll confirm whether we can help.</p>
    </div>
    <figure class="s-photo a-img"><img src="assets/services/area.jpg" alt="Rooftop HVAC unit on a Las Vegas home with neighborhood rooftops and palm trees beyond" width="380" height="300" loading="lazy" decoding="async"></figure>
  </div>
</section>

<!-- ===== 10 · FAQ ===== -->
<section class="s-sec" aria-labelledby="faq-title">
  <div class="wrap">
    <header class="s-head s-head--center">
      <p class="a-label" data-a><span>09</span>FAQ</p>
      <h2 id="faq-title" class="a-h2" data-split>Frequently Asked <em>Questions</em></h2>
    </header>
    {faq_html(SFAQ)}
  </div>
</section>

<!-- ===== 11 · FINAL CTA ===== -->
<section class="s-cta" aria-labelledby="scta-title">
  <div class="wrap">
    <div class="s-cta__card">
      <h2 id="scta-title" class="a-h2" data-split>Ready to Restore <em>Your Comfort?</em></h2>
      <p class="s-cta__lead" data-a>Whether you need a repair, a new installation or routine maintenance, Cosmos is ready to help.</p>
      <div class="s-btns" data-a>
        <a class="btn btn--caps" href="{BOOK}" target="_blank" rel="noopener">Schedule a Service {ARROW}</a>
        <a class="btn btn--caps btn--ghost-light" href="tel:+17029605555">{icon('i-phone','ic')}Call Cosmos Today</a>
      </div>
    </div>
  </div>
</section>

</main>
'''+FOOTER+TAIL
    open('services.html','w').write(set_active(h,'Services'))

# =========================== COMFORT CLUB ===========================
CFAQ=[
 ("What is Cosmo’s Comfort Club?","Cosmo’s Comfort Club is our year-round HVAC maintenance membership, built around proactive care for your heating and cooling system and backed by the Cosmo’s Comfort Guarantee™."),
 ("What does membership include?","Membership is designed around tune-ups that help keep your system running like new, priority scheduling and exclusive member discounts. Specific plan details are confirmed by our team, so please contact us for the current membership terms."),
 ("How often is maintenance performed?","Visit frequency depends on the membership plan you choose. Contact our team and we’ll confirm the schedule that applies to you."),
 ("How do I join?","Call us at +1 (702) 960-5555, email service@cosmosaclv.com or use the contact form on our homepage, and our team will walk you through enrolling."),
 ("Can I enroll an existing HVAC system?","Please contact our team with details about your system and we’ll confirm how membership would apply to it."),
 ("How can I contact Cosmos about membership?","Call +1 (702) 960-5555, email service@cosmosaclv.com or visit us at 10161 W Park Run Dr #150, Las Vegas, NV 89145."),
]
def club():
    ld=json.dumps({"@context":"https://schema.org","@graph":[
        {"@type":"WebPage","@id":"https://www.cosmosaclv.com/comfort-club.html#page","url":"https://www.cosmosaclv.com/comfort-club.html","name":"Cosmo’s Comfort Club HVAC Maintenance Membership","isPartOf":{"@id":"https://www.cosmosaclv.com/#business"}},
        crumbs("Cosmo’s Comfort Club","comfort-club.html"),BUSINESS,faq_ld(CFAQ)]},ensure_ascii=False)
    h=head("Cosmo’s Comfort Club | HVAC Maintenance Membership in Las Vegas",
      "Join Cosmo’s Comfort Club for year-round HVAC maintenance in Las Vegas, Henderson and North Las Vegas — proactive care, priority scheduling and peace of mind from Cosmos.",
      "comfort-club.html","Cosmo’s Comfort Club | Year-Round HVAC Protection in Las Vegas",ld)
    benefits=[("s-cal","Scheduled HVAC Maintenance","Regular tune-ups that help keep your heating and cooling system running like new."),
      ("s-snow","Seasonal System Inspections","Check-ups timed for the seasons that put the most demand on your equipment."),
      ("a-clock","Priority Service Scheduling","Members are given priority when scheduling service with our team."),
      ("a-gauge","Professional System Checks","A trained technician reviews how your equipment is performing."),
      ("s-alert","Early Identification of Potential Issues","Spotting small concerns early helps avoid bigger surprises later."),
      ("a-heart","Ongoing Comfort Support","A local team you know and can call all year long.")]
    bhtml='\n'.join(f'      <li class="c-benefit" data-a{" style=\"--d:%.2fs\""%((i%3)*.1) if i%3 else ""}><span class="c-benefit__no" aria-hidden="true">0{i+1}</span>{icon(ic,"c-benefit__ic")}<h3>{t}</h3><p>{d}</p></li>' for i,(ic,t,d) in enumerate(benefits))
    h+=SPRITE+HEADER+f'''<main id="main" class="about-page">

<!-- ===== 1 · HERO ===== -->
<section class="c-hero" aria-labelledby="c-hero-title">
  <div class="wrap c-hero__grid">
    <div>
      <p class="a-eyebrow" data-a>Cosmo’s Comfort Club</p>
      <h1 id="c-hero-title" class="a-display" data-split>Year-Round Protection <em>for Your Comfort.</em></h1>
      <p class="c-hero__lead" data-a style="--d:.4s">Enjoy greater peace of mind with proactive HVAC maintenance and dependable care designed to help keep your heating and cooling system running smoothly throughout the year.</p>
      <div class="s-btns" data-a style="--d:.55s">
        <a class="btn btn--caps" href="#benefits">Explore Membership Benefits {ARROW}</a>
        <a class="btn btn--caps btn--ghost-light" href="index.html#contact">Join the Comfort Club</a>
      </div>
    </div>
    <div class="c-hero__media">
      <figure class="s-photo c-hero__photo a-img"><img src="assets/club/hero.jpg" alt="Cosmo’s HVAC technician inspecting a commercial rooftop air conditioning unit" width="349" height="461" decoding="async"></figure>
      <p class="c-hero__seal" data-a style="--d:.5s"><span><b>Comfort<br>Guarantee™</b>Cosmo’s</span></p>
    </div>
  </div>
  <svg class="a-wave" viewBox="0 0 1440 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0 40c240 30 480 30 720 8s480-30 720 0v12H0z" fill="#fff"/></svg>
</section>

<!-- ===== 2 · INTRODUCTION ===== -->
<section class="s-sec c-intro" aria-labelledby="c-intro-title">
  <div class="wrap c-intro__grid">
    <figure class="s-photo a-img"><img src="assets/club/intro.jpg" alt="Technician on a ladder checking ceiling-mounted HVAC equipment during a maintenance visit" width="260" height="224" loading="lazy" decoding="async"></figure>
    <div>
      <p class="a-label" data-a><span>01</span>Why a membership</p>
      <h2 id="c-intro-title" class="a-h2" data-split>Comfort Is Better <em>When It’s Protected.</em></h2>
      <p class="a-lead" data-a>Heating and cooling systems work hard, especially in the Las Vegas climate. Proactive care helps you stay ahead of problems instead of reacting to them.</p>
      <ul class="s-list" data-a><li>Regular system inspections</li><li>Preventative maintenance</li><li>Improved equipment reliability</li><li>Early identification of potential issues</li><li>Greater peace of mind</li></ul>
    </div>
  </div>
</section>

<!-- ===== 3 · BENEFITS =====
     VERIFY: Priority scheduling, tune-ups and member discounts come from the live website. The other benefit
     descriptions are general preventative-care wording — confirm against your actual Comfort Club agreement. -->
<section class="s-sec s-sec--mint" id="benefits" aria-labelledby="c-ben-title">
  <div class="wrap">
    <header class="s-head s-head--center">
      <p class="a-label" data-a><span>02</span>Membership benefits</p>
      <h2 id="c-ben-title" class="a-h2" data-split>More Care. More Confidence. <em>More Comfort.</em></h2>
    </header>
    <ul class="c-benefits">
{bhtml}
    </ul>
  </div>
</section>

<!-- ===== 4 · HOW IT WORKS ===== -->
<section class="s-sec" aria-labelledby="c-how-title">
  <div class="wrap">
    <header class="s-head">
      <p class="a-label" data-a><span>03</span>How it works</p>
      <h2 id="c-how-title" class="a-h2" data-split>How the <em>Comfort Club Works.</em></h2>
    </header>
    <ol class="a-steps" data-progress>
      <li class="a-step" data-a><span class="a-step__no" aria-hidden="true">01</span><h3>Choose Your Membership</h3><p>Talk with our team about the plan that fits your home.</p></li>
      <li class="a-step" data-a style="--d:.12s"><span class="a-step__no" aria-hidden="true">02</span><h3>Schedule Your Maintenance</h3><p>We arrange your maintenance visit at a time that works for you.</p></li>
      <li class="a-step" data-a style="--d:.24s"><span class="a-step__no" aria-hidden="true">03</span><h3>Receive Professional Care</h3><p>A trained technician inspects and tunes up your system.</p></li>
      <li class="a-step" data-a style="--d:.36s"><span class="a-step__no" aria-hidden="true">04</span><h3>Enjoy Greater Peace of Mind</h3><p>Stay comfortable knowing your system is being looked after.</p></li>
    </ol>
  </div>
</section>

<!-- ===== 5 · WHY MAINTENANCE MATTERS ===== -->
<section class="s-sec s-sec--cream c-why" aria-labelledby="c-why-title">
  <div class="wrap c-why__grid">
    <div class="c-why__photos">
      <figure class="s-photo a-img"><img src="assets/club/care-1.jpg" alt="Technician’s hand replacing a dirty air filter inside an HVAC system" width="303" height="224" loading="lazy" decoding="async"></figure>
      <figure class="s-photo s-photo--inset a-img" style="--d:.2s"><img src="assets/club/care-2.jpg" alt="Packaged rooftop HVAC unit on a home’s roof awaiting seasonal maintenance" width="360" height="360" loading="lazy" decoding="async"></figure>
    </div>
    <div>
      <p class="a-label" data-a><span>04</span>Preventative maintenance</p>
      <h2 id="c-why-title" class="a-h2" data-split>Small Maintenance Steps. <em>Long-Term Comfort.</em></h2>
      <ul class="c-points" data-a>
        <li><b>Regular inspections matter</b><span>A trained eye can notice wear and changes in performance before they become breakdowns.</span></li>
        <li><b>Neglected equipment struggles</b><span>Dirty filters and unchecked components make systems work harder than they should.</span></li>
        <li><b>Seasonal maintenance pays off</b><span>Preparing for summer and winter helps your system meet the demands of each season.</span></li>
        <li><b>Professional servicing supports performance</b><span>Proper tune-ups help your equipment run the way it was designed to.</span></li>
      </ul>
    </div>
  </div>
</section>

<!-- ===== 6 · PLANS (enquiry-based; editable) ===== -->
<section class="s-sec" id="plans" aria-labelledby="c-plan-title">
  <div class="wrap">
    <header class="s-head s-head--center">
      <p class="a-label" data-a><span>05</span>Membership plans</p>
      <h2 id="c-plan-title" class="a-h2" data-split>Find the Right <em>Comfort Plan.</em></h2>
      <p class="a-lead" data-a>Membership details are tailored to your system. Our team will confirm current plans and pricing with you directly.</p>
    </header>
    <!-- EDIT HERE: replace each <dd> with your real plan details (name, price, billing, visits, services, extras).
         Duplicate a <article class="c-plan"> block to add more plans. No prices are shown until you add them. -->
    <div class="c-plans">
      <article class="c-plan c-plan--main" data-a>
        <p class="c-plan__badge">Cosmo’s Comfort Club</p>
        <h3>Comfort Club Membership</h3>
        <dl>
          <div><dt>Pricing</dt><dd>Contact us for current pricing</dd></div>
          <div><dt>Billing</dt><dd>Confirmed when you enroll</dd></div>
          <div><dt>Maintenance visits</dt><dd>Confirmed by plan</dd></div>
          <div><dt>Included</dt><dd>Tune-ups, priority scheduling and member discounts</dd></div>
          <div><dt>Backed by</dt><dd>The Cosmo’s Comfort Guarantee™</dd></div>
        </dl>
        <a class="btn btn--caps" href="index.html#contact">Join the Comfort Club {ARROW}</a>
      </article>
      <aside class="c-plan c-plan--aside" data-a style="--d:.15s">
        <h3>Not sure which plan fits?</h3>
        <p>Tell us about your home and your system and we’ll recommend the right level of care — no pressure.</p>
        <div class="s-btns"><a class="btn btn--caps" href="tel:+17029605555">{icon('i-phone','ic')}Call +1 (702) 960-5555</a></div>
      </aside>
    </div>
  </div>
</section>

<!-- ===== 7 · TRUST ===== -->
<section class="s-sec s-sec--sky" aria-labelledby="c-trust-title">
  <div class="wrap">
    <header class="s-head s-head--center">
      <p class="a-label" data-a><span>06</span>Customer trust</p>
      <h2 id="c-trust-title" class="a-h2" data-split>Comfort That Continues <em>Beyond the Appointment.</em></h2>
    </header>
    <ul class="c-trust">
      <li data-a><b>5.0</b><span>Google rating</span></li>
      <li data-a style="--d:.08s"><b>10</b><span>Google reviews</span></li>
      <li data-a style="--d:.16s"><b>12<small>+</small></b><span>Years hands-on experience</span></li>
      <li data-a style="--d:.24s"><b>#0095036</b><span>Licensed contractor</span></li>
    </ul>
    <p class="c-trust__link" data-a><a class="a-link-dark" href="index.html#reviews">Read what customers say {ARROW}</a></p>
  </div>
</section>

<!-- ===== 8 · FAQ ===== -->
<section class="s-sec" aria-labelledby="c-faq-title">
  <div class="wrap">
    <header class="s-head s-head--center">
      <p class="a-label" data-a><span>07</span>FAQ</p>
      <h2 id="c-faq-title" class="a-h2" data-split>Comfort Club <em>Questions</em></h2>
    </header>
    {faq_html(CFAQ)}
  </div>
</section>

<!-- ===== 9 · FINAL CTA (orange) ===== -->
<section class="a-cta" id="contact-cta" aria-labelledby="c-cta-title">
  <div class="wrap">
    <div class="a-cta__card">
      <div class="a-cta__text">
        <p class="a-label a-label--light" data-a><span>08</span>Join today</p>
        <h2 id="c-cta-title" class="a-h2 a-h2--light" data-split>Let’s Create a More <em>Comfortable Environment.</em></h2>
        <p class="a-cta__lead" data-a>Take a proactive approach to your home’s comfort with professional HVAC maintenance from Cosmos.</p>
        <div class="a-cta__actions" data-a>
          <a class="btn btn--caps a-btn--white" href="index.html#contact">Join the Comfort Club {ARROW}</a>
          <a class="a-link-light" href="index.html#contact">Contact Our Team</a>
        </div>
      </div>
      <ul class="a-cta__info" data-a style="--d:.2s" aria-label="Contact details">
        <li>{icon('i-phone','ic')}<a href="tel:+17029605555">+1 (702) 960-5555</a></li>
        <li>{icon('i-mail','ic')}<a href="mailto:service@cosmosaclv.com">service@cosmosaclv.com</a></li>
        <li>{icon('i-pin','ic')}<a href="https://www.google.com/maps/search/?api=1&amp;query=10161+W+Park+Run+Dr+%23150,+Las+Vegas,+NV+89145" target="_blank" rel="noopener">10161 W Park Run Dr #150<br>Las Vegas, NV 89145</a></li>
      </ul>
    </div>
  </div>
</section>

</main>
'''+FOOTER+TAIL
    open('comfort-club.html','w').write(set_active(h,'Cosmo’s Comfort Club'))

services(); club(); print('built')
