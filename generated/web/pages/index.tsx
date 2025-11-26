import Head from "next/head";
import { useMemo, useState } from "react";

type LangCode =
  | "en"
  | "fr"
  | "nl"
  | "de"
  | "es"
  | "pt"
  | "hi"
  | "ml"
  | "ta"
  | "ar"
  | "zh"
  | "ja"
  | "ru";

interface Translation {
  title: string;
  subtitle: string;
  ctaPrimary: string;
  ctaSecondary: string;
  sectionTitle: string;
  features: string[];
  footer: string;
}

// Language selector options
const LANGUAGE_OPTIONS: { code: LangCode; label: string }[] = [
  { code: "en", label: "English" },
  { code: "fr", label: "Français" },
  { code: "nl", label: "Nederlands" },
  { code: "de", label: "Deutsch" },
  { code: "es", label: "Español" },
  { code: "pt", label: "Português" },
  { code: "hi", label: "हिन्दी (Hindi)" },
  { code: "ml", label: "മലയാളം (Malayalam)" },
  { code: "ta", label: "தமிழ் (Tamil)" },
  { code: "ar", label: "العربية (Arabic)" },
  { code: "zh", label: "中文 (Chinese)" },
  { code: "ja", label: "日本語 (Japanese)" },
  { code: "ru", label: "Русский (Russian)" },
];

// Base English text (fallback)
const ENGLISH_BASE: Translation = {
  title: "Online travel booking for flights and hotels",
  subtitle:
    "Plan your next trip with flexible search, secure booking, and real-time updates.",
  ctaPrimary: "Start planning",
  ctaSecondary: "Explore destinations",
  sectionTitle: "What you can do on this site",
  features: [
    "Build a complete travel plan with flights and hotels",
    "Search and filter by budget, dates, airlines, and rating",
    "Contact support when you need help with a booking",
    "Use admin tools for managing trips and customers",
  ],
  footer: "Built with Next.js, FastAPI, and SQLite.",
};

// Per-language overrides (only keys that differ from ENGLISH_BASE)
const TRANSLATIONS: Partial<Record<LangCode, Partial<Translation>>> = {
  en: {},
  fr: {
    title: "Réservation de voyages en ligne (vols et hôtels)",
    subtitle:
      "Préparez votre prochain voyage avec une recherche flexible, une réservation sécurisée et des mises à jour en temps réel.",
    ctaPrimary: "Commencer à planifier",
    ctaSecondary: "Explorer les destinations",
    sectionTitle: "Ce que vous pouvez faire sur ce site",
    features: [
      "Construire un itinéraire complet avec vols et hôtels",
      "Rechercher et filtrer par budget, dates, compagnies aériennes et note",
      "Contacter le support en cas de problème avec une réservation",
      "Utiliser des outils d’administration pour gérer voyages et clients",
    ],
    footer: "Construit avec Next.js, FastAPI et SQLite.",
  },
  nl: {
    title: "Online reizen boeken voor vluchten en hotels",
    subtitle:
      "Plan je volgende reis met flexibele zoekopties, veilige boeking en realtime updates.",
    ctaPrimary: "Begin met plannen",
    ctaSecondary: "Bestemmingen verkennen",
    sectionTitle: "Wat je op deze site kunt doen",
    features: [
      "Maak een volledig reisplan met vluchten en hotels",
      "Zoek en filter op budget, data, luchtvaartmaatschappij en beoordeling",
      "Neem contact op met support bij vragen over je boeking",
      "Gebruik admintools om reizen en klanten te beheren",
    ],
    footer: "Gebouwd met Next.js, FastAPI en SQLite.",
  },
  de: {
    title: "Online Reisebuchung für Flüge und Hotels",
    subtitle:
      "Plane deine nächste Reise mit flexibler Suche, sicherer Buchung und Echtzeit-Updates.",
    ctaPrimary: "Reise planen",
    ctaSecondary: "Ziele entdecken",
  },
  es: {
    title: "Reserva de viajes en línea para vuelos y hoteles",
    subtitle:
      "Planifica tu próximo viaje con búsqueda flexible, reserva segura y actualizaciones en tiempo real.",
    ctaPrimary: "Comenzar a planear",
    ctaSecondary: "Explorar destinos",
  },
  pt: {
    title: "Reserva de viagens online para voos e hotéis",
    subtitle:
      "Planeje sua próxima viagem com busca flexível, reserva segura e atualizações em tempo real.",
    ctaPrimary: "Começar a planejar",
    ctaSecondary: "Explorar destinos",
  },
  hi: {
    title: "ऑनलाइन ट्रैवल बुकिंग (फ्लाइट और होटल)",
    subtitle:
      "लचीली खोज, सुरक्षित बुकिंग और रियल-टाइम अपडेट के साथ अपनी अगली यात्रा की योजना बनाएं।",
    ctaPrimary: "योजना शुरू करें",
    ctaSecondary: "डेस्टिनेशन देखें",
  },
  ml: {
    title: "ഓൺലൈൻ ട്രാവൽ ബുക്കിംഗ് (വിമാനങ്ങളും ഹോട്ടലുകളും)",
    subtitle:
      "ഇഷ്ടാനുസൃത തിരച്ചിൽ, സുരക്ഷിത ബുക്കിംഗ്, റിയൽ-ടൈം അപ്ഡേറ്റുകൾ എന്നിവയോടെ നിങ്ങളുടെ അടുത്ത യാത്ര പ്ലാൻ ചെയ്യൂ.",
    ctaPrimary: "യാത്ര പ്ലാൻ ചെയ്യുക",
    ctaSecondary: "ഗമ്യസ്ഥലങ്ങൾ കാണുക",
    sectionTitle: "ഈ സൈറ്റിൽ നിങ്ങൾക്ക് ചെയ്യാനാകുന്നത്",
    features: [
      "വിമാനങ്ങളും ഹോട്ടലുകളും ചേർത്ത് പൂർണ്ണ യാത്രാപദ്ധതി തയ്യാറാക്കുക",
      "ബജറ്റ്, തീയതി, എയർലൈൻസ്, റേറ്റിംഗ് എന്നിവ പ്രകാരം തിരയാനും ഫിൽറ്റർ ചെയ്യാനും കഴിയൂ",
      "ബുക്കിംഗുമായി ബന്ധപ്പെട്ട സഹായത്തിനായി സപ്പോർട്ട് ടീമിനെ സമീപിക്കുക",
      "ട്രിപ്പുകളും കസ്റ്റമർമാരും മാനേജ് ചെയ്യാൻ അഡ്മിൻ ടൂളുകൾ ഉപയോഗിക്കുക",
    ],
  },
  ta: {
    title: "ஆன்லைன் பயண முன்பதிவு (விமானம் & ஹோட்டல்)",
    subtitle:
      "நெகிழ்வான தேடல், பாதுகாப்பான முன்பதிவு, நேரடி புதுப்பிப்புகளுடன் உங்கள் அடுத்த பயணத்தை திட்டமிடுங்கள்.",
  },
  ar: {
    title: "حجز السفر عبر الإنترنت للرحلات والفنادق",
    subtitle:
      "خطط لرحلتك القادمة مع بحث مرن، حجز آمن وتحديثات لحظية.",
  },
  zh: {
    title: "机票与酒店一站式在线预订",
    subtitle: "通过灵活搜索、安全预订和实时更新来规划您的下一次旅行。",
  },
  ja: {
    title: "フライトとホテルのオンライン旅行予約",
    subtitle:
      "柔軟な検索、安全な予約、リアルタイム更新で次の旅行を計画しましょう。",
  },
  ru: {
    title: "Онлайн-бронирование путешествий (авиабилеты и отели)",
    subtitle:
      "Планируйте своё следующее путешествие с гибким поиском, безопасным бронированием и обновлениями в реальном времени.",
  },
};

function resolveTranslation(lang: LangCode): Translation {
  const overrides = TRANSLATIONS[lang] || {};
  return {
    ...ENGLISH_BASE,
    ...overrides,
    features: overrides.features || ENGLISH_BASE.features,
  };
}

export default function HomePage() {
  const [lang, setLang] = useState<LangCode>("en");

  const t = useMemo(() => resolveTranslation(lang), [lang]);

  return (
    <>
      <Head>
        <title>online_travel – Multilingual landing</title>
      </Head>
      <main className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-slate-50">
        <div className="mx-auto flex min-h-screen max-w-5xl flex-col px-4 py-8">
          {/* Top bar */}
          <header className="mb-8 flex items-center justify-between">
            <div className="flex flex-col">
              <span className="text-xs font-semibold tracking-[0.2em] text-sky-400 uppercase">
                online_travel
              </span>
              <span className="text-sm text-slate-400">
                Next.js + FastAPI + SQLite
              </span>
            </div>

            {/* Language selector */}
            <div className="flex items-center gap-2">
              <label
                htmlFor="language-select"
                className="text-xs font-medium text-slate-300"
              >
                Language
              </label>
              <select
                id="language-select"
                value={lang}
                onChange={(e) => setLang(e.target.value as LangCode)}
                className="rounded-md border border-slate-700 bg-slate-900/80 px-2 py-1 text-xs text-slate-100 shadow-sm outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500"
              >
                {LANGUAGE_OPTIONS.map((opt) => (
                  <option key={opt.code} value={opt.code}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>
          </header>

          {/* Hero + content */}
          <div className="flex flex-1 flex-col gap-10 md:flex-row">
            {/* Left: text */}
            <section className="flex flex-1 flex-col justify-center gap-6">
              <h1 className="text-3xl font-semibold tracking-tight text-slate-50 sm:text-4xl md:text-5xl">
                {t.title}
              </h1>
              <p className="max-w-xl text-sm leading-relaxed text-slate-300 sm:text-base">
                {t.subtitle}
              </p>

              <div className="flex flex-wrap gap-3">
                <a
                  href="/flights"
                  className="inline-flex items-center justify-center rounded-full border border-transparent bg-sky-500 px-5 py-2 text-sm font-medium text-slate-950 shadow-sm transition hover:bg-sky-400"
                >
                  {t.ctaPrimary}
                </a>
                <a
                  href="/hotels"
                  className="inline-flex items-center justify-center rounded-full border border-slate-700 bg-slate-900/60 px-5 py-2 text-sm font-medium text-slate-100 shadow-sm transition hover:border-sky-500 hover:text-sky-100"
                >
                  {t.ctaSecondary}
                </a>
              </div>

              <div className="mt-4 flex flex-wrap gap-2 text-xs text-slate-400">
                <span className="rounded-full border border-slate-700 bg-slate-900/80 px-3 py-1">
                  ✈️ Flights + hotels
                </span>
                <span className="rounded-full border border-slate-700 bg-slate-900/80 px-3 py-1">
                  🔐 Secure booking
                </span>
                <span className="rounded-full border border-slate-700 bg-slate-900/80 px-3 py-1">
                  🌍 Multi-language ready
                </span>
              </div>
            </section>

            {/* Right: features card */}
            <section className="flex flex-1 items-center justify-center">
              <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900/70 p-5 shadow-xl shadow-slate-950/40">
                <h2 className="mb-3 text-sm font-semibold text-slate-100">
                  {t.sectionTitle}
                </h2>
                <ul className="space-y-2 text-xs text-slate-300">
                  {t.features.map((feature, idx) => (
                    <li key={idx} className="flex gap-2">
                      <span className="mt-[2px] text-sky-400">•</span>
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>

                <div className="mt-5 rounded-lg border border-slate-800 bg-slate-950/60 px-3 py-2 text-[11px] text-slate-400">
                  <div className="mb-1 font-medium text-slate-200">
                    Tech stack
                  </div>
                  <div>Frontend: Next.js (TypeScript)</div>
                  <div>Backend: FastAPI (Python)</div>
                  <div>Database: SQLite</div>
                </div>
              </div>
            </section>
          </div>

          {/* Footer */}
          <footer className="mt-8 border-t border-slate-800 pt-4 text-xs text-slate-500">
            {t.footer}{" "}
            <span className="text-slate-400">
              Choose any language above — UI text falls back to English where a
              translation is not defined yet.
            </span>
          </footer>
        </div>
      </main>
    </>
  );
}
