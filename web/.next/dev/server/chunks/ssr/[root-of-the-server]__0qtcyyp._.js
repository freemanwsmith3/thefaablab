module.exports = [
"[externals]/next/dist/shared/lib/no-fallback-error.external.js [external] (next/dist/shared/lib/no-fallback-error.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/shared/lib/no-fallback-error.external.js", () => require("next/dist/shared/lib/no-fallback-error.external.js"));

module.exports = mod;
}),
"[project]/web/app/waiver-wire/[season]/[week]/page.js [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>WeekPage,
    "generateMetadata",
    ()=>generateMetadata,
    "revalidate",
    ()=>revalidate
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/web/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-jsx-dev-runtime.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/web/node_modules/next/dist/client/app-dir/link.react-server.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$image$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/web/node_modules/next/image.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$api$2f$navigation$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$locals$3e$__ = __turbopack_context__.i("[project]/web/node_modules/next/dist/api/navigation.react-server.js [app-rsc] (ecmascript) <locals>");
var __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$client$2f$components$2f$navigation$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/web/node_modules/next/dist/client/components/navigation.react-server.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$lib$2f$api$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/web/lib/api.js [app-rsc] (ecmascript)");
;
;
;
;
;
const revalidate = 300;
async function generateMetadata({ params }) {
    const { season, week } = await params;
    const data = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$lib$2f$api$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["getWeek"])(season, week);
    if (!data) return {
        title: `Week ${week} waiver wire`
    };
    const names = data.players.slice(0, 5).map((p)=>p.name).join(', ');
    return {
        title: `Week ${week} FAAB waiver wire bids (${season})`,
        description: `What to bid on Week ${week} waiver targets: ${names}. Crowd-sourced FAAB ` + `bids plus real Sleeper league results, shown in your league's dollars.`,
        alternates: {
            canonical: `/waiver-wire/${season}/${week}`
        },
        openGraph: {
            title: `Week ${week} FAAB waiver wire bids`,
            description: `Median bids and winning ranges for ${data.players.length} waiver targets.`
        }
    };
}
async function WeekPage({ params }) {
    const { season, week } = await params;
    const data = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$lib$2f$api$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["getWeek"])(season, week);
    if (!data || !data.players.length) (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$client$2f$components$2f$navigation$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["notFound"])();
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("main", {
        style: {
            maxWidth: 1180,
            margin: '0 auto',
            padding: '20px 14px 60px'
        },
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                style: {
                    fontSize: 26,
                    color: '#035e7b',
                    margin: '0 0 6px'
                },
                children: [
                    "Week ",
                    data.week,
                    " FAAB waiver wire bids"
                ]
            }, void 0, true, {
                fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
                lineNumber: 33,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                style: {
                    color: '#4d707c',
                    maxWidth: '46ch',
                    margin: '0 0 20px'
                },
                children: [
                    "What the crowd and real Sleeper leagues are paying for each ",
                    season,
                    " Week",
                    ' ',
                    data.week,
                    " waiver target. Bids are percent of budget, so they compare across leagues."
                ]
            }, void 0, true, {
                fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
                lineNumber: 36,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
                style: {
                    listStyle: 'none',
                    padding: 0,
                    display: 'grid',
                    gap: 12,
                    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))'
                },
                children: data.players.map((p)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                        style: {
                            background: '#fff',
                            border: '2px solid #035e7b',
                            borderRadius: 8,
                            padding: 14
                        },
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"], {
                                    href: `/waiver-wire/${season}/${week}/${p.slug}`,
                                    style: {
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: 12
                                    },
                                    children: [
                                        p.image && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$image$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"], {
                                            src: p.image,
                                            alt: `${p.name} headshot`,
                                            width: 56,
                                            height: 56,
                                            style: {
                                                objectFit: 'contain',
                                                background: '#e6eff2',
                                                borderRadius: 6
                                            }
                                        }, void 0, false, {
                                            fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
                                            lineNumber: 51,
                                            columnNumber: 19
                                        }, this),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                                    style: {
                                                        fontSize: 18,
                                                        color: '#035e7b',
                                                        margin: 0
                                                    },
                                                    children: p.name
                                                }, void 0, false, {
                                                    fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
                                                    lineNumber: 55,
                                                    columnNumber: 19
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                    style: {
                                                        fontSize: 14,
                                                        color: '#035e7b',
                                                        fontWeight: 600
                                                    },
                                                    children: p.meta
                                                }, void 0, false, {
                                                    fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
                                                    lineNumber: 56,
                                                    columnNumber: 19
                                                }, this)
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
                                            lineNumber: 54,
                                            columnNumber: 17
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
                                    lineNumber: 48,
                                    columnNumber: 15
                                }, this),
                                p.hasData && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                    style: {
                                        margin: '10px 0 0',
                                        fontSize: 14,
                                        color: '#4d707c'
                                    },
                                    children: [
                                        "Median bid ",
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                            children: [
                                                p.median,
                                                "%"
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
                                            lineNumber: 61,
                                            columnNumber: 30
                                        }, this),
                                        " of budget from",
                                        ' ',
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                            children: p.count.toLocaleString()
                                        }, void 0, false, {
                                            fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
                                            lineNumber: 62,
                                            columnNumber: 19
                                        }, this),
                                        " bids",
                                        p.sleeper && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Fragment"], {
                                            children: [
                                                " · Sleeper leagues paid ",
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                    children: [
                                                        p.sleeper.pct,
                                                        "%"
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
                                                    lineNumber: 64,
                                                    columnNumber: 47
                                                }, this),
                                                " across",
                                                ' ',
                                                p.sleeper.leagues,
                                                " leagues"
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
                                            lineNumber: 64,
                                            columnNumber: 21
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
                                    lineNumber: 60,
                                    columnNumber: 17
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
                            lineNumber: 47,
                            columnNumber: 13
                        }, this)
                    }, p.id, false, {
                        fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
                        lineNumber: 45,
                        columnNumber: 11
                    }, this))
            }, void 0, false, {
                fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
                lineNumber: 42,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/web/app/waiver-wire/[season]/[week]/page.js",
        lineNumber: 32,
        columnNumber: 5
    }, this);
}
}),
"[project]/web/app/waiver-wire/[season]/[week]/page.js [app-rsc] (ecmascript, Next.js Server Component)", (function(__turbopack_context__){

__turbopack_context__.n(__turbopack_context__.i("[project]/web/app/waiver-wire/[season]/[week]/page.js [app-rsc] (ecmascript)"));
}),
"[project]/web/lib/api.js [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "buildMeta",
    ()=>buildMeta,
    "getCurrentWeek",
    ()=>getCurrentWeek,
    "getOpponent",
    ()=>getOpponent,
    "getPlayer",
    ()=>getPlayer,
    "getWeek",
    ()=>getWeek
]);
/**
 * Server-side data access.
 *
 * Everything here runs on the server, so the HTML a crawler receives already
 * contains player names and bid figures -- the whole point of the migration.
 *
 * cache() dedupes within a single render pass: generateMetadata and the page
 * body both need the same week, and without it that would be two fetches.
 */ var __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/web/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$lib$2f$schedule2026$2e$json$2e5b$json$5d2e$cjs__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/web/lib/schedule2026.json.[json].cjs [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$lib$2f$slug$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/web/lib/slug.js [app-rsc] (ecmascript)");
;
;
;
const API = process.env.FAAB_API_URL || 'http://127.0.0.1:8000/api/';
// Aggregates only change when a bid lands or the weekly ingest runs, so the
// rendered page can be reused for a while rather than refetched per visitor.
const REVALIDATE = Number(process.env.FAAB_REVALIDATE || 300);
const SCHEDULE = {
    2026: __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$lib$2f$schedule2026$2e$json$2e5b$json$5d2e$cjs__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"]
};
function getOpponent(abbr, week, season) {
    const table = SCHEDULE[season];
    if (!table || !abbr) return null;
    return (table[abbr] || {})[String(week)] || null;
}
function buildMeta(position, abbr, opponent, week) {
    const head = [
        position,
        abbr
    ].filter(Boolean).join(' - ');
    if (!opponent) return `${head} · Week ${week}`;
    return `${head} ${opponent.isHome ? 'vs' : 'at'} ${opponent.abbr} in Week ${week}`;
}
/** Fewer leagues than this and the Sleeper figure is not worth showing. */ const SLEEPER_MIN_LEAGUES = 10;
function toViewModel(p, season, week) {
    const crowd = p.crowd;
    const buckets = (crowd?.bins || []).map((b)=>({
            loPct: b.lo,
            hiPct: b.hi,
            bids: b.bids
        }));
    // Outliers are trimmed before binning, so report the post-trim total; that
    // is what makes bucket shares sum to 100%.
    const trimmedTotal = buckets.reduce((s, b)=>s + b.bids, 0);
    const opponent = getOpponent(p.team, week, season);
    const market = p.market;
    return {
        id: p.id,
        name: p.name,
        slug: (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$lib$2f$slug$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["slugify"])(p.name),
        abbr: p.team || null,
        position: p.position || null,
        image: p.image || null,
        meta: buildMeta(p.position, p.team, opponent, week),
        hasData: !!(crowd && crowd.n),
        median: crowd?.median ?? null,
        mode: crowd?.mode ?? null,
        count: trimmedTotal,
        buckets,
        sleeper: market && market.n_leagues >= SLEEPER_MIN_LEAGUES && market.mean != null ? {
            pct: market.mean,
            leagues: market.n_leagues,
            bidToWin80: market.bid_to_win_80
        } : null
    };
}
const getWeek = (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["cache"])(async (season, week)=>{
    const url = `${API}week?season=${season}&week=${week}&limit=200`;
    const res = await fetch(url, {
        next: {
            revalidate: REVALIDATE
        }
    });
    if (!res.ok) return null;
    const data = await res.json();
    return {
        season: data.season ?? Number(season),
        week: data.week ?? Number(week),
        players: (data.players || []).map((p)=>toViewModel(p, Number(season), Number(week)))
    };
});
const getPlayer = (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["cache"])(async (season, week, slug)=>{
    const wk = await getWeek(season, week);
    if (!wk) return null;
    return wk.players.find((p)=>p.slug === slug) || null;
});
const getCurrentWeek = (0, __TURBOPACK__imported__module__$5b$project$5d2f$web$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["cache"])(async ()=>{
    try {
        const res = await fetch('https://api.sleeper.app/v1/state/nfl', {
            next: {
                revalidate: 3600
            }
        });
        if (!res.ok) throw new Error('state unavailable');
        const s = await res.json();
        const week = Math.min(Math.max(Number(s.week) || 1, 1), 18);
        return {
            season: Number(s.season) || new Date().getFullYear(),
            week
        };
    } catch  {
        return {
            season: new Date().getFullYear(),
            week: 1
        };
    }
});
}),
"[project]/web/lib/schedule2026.json.[json].cjs [app-rsc] (ecmascript)", ((__turbopack_context__, module, exports) => {

module.exports = JSON.parse("{\"ARI\":{\"1\":{\"abbr\":\"LAC\",\"isHome\":false},\"10\":{\"abbr\":\"LAR\",\"isHome\":true},\"11\":{\"abbr\":\"KC\",\"isHome\":false},\"12\":{\"abbr\":\"WAS\",\"isHome\":true},\"13\":{\"abbr\":\"PHI\",\"isHome\":true},\"15\":{\"abbr\":\"NYJ\",\"isHome\":true},\"16\":{\"abbr\":\"NO\",\"isHome\":false},\"17\":{\"abbr\":\"LV\",\"isHome\":true},\"18\":{\"abbr\":\"SF\",\"isHome\":true},\"2\":{\"abbr\":\"SEA\",\"isHome\":true},\"3\":{\"abbr\":\"SF\",\"isHome\":false},\"4\":{\"abbr\":\"NYG\",\"isHome\":false},\"5\":{\"abbr\":\"DET\",\"isHome\":true},\"6\":{\"abbr\":\"LAR\",\"isHome\":false},\"7\":{\"abbr\":\"DEN\",\"isHome\":true},\"8\":{\"abbr\":\"DAL\",\"isHome\":false},\"9\":{\"abbr\":\"SEA\",\"isHome\":false}},\"ATL\":{\"1\":{\"abbr\":\"PIT\",\"isHome\":false},\"10\":{\"abbr\":\"KC\",\"isHome\":true},\"12\":{\"abbr\":\"MIN\",\"isHome\":false},\"13\":{\"abbr\":\"DET\",\"isHome\":true},\"14\":{\"abbr\":\"CLE\",\"isHome\":false},\"15\":{\"abbr\":\"WAS\",\"isHome\":false},\"16\":{\"abbr\":\"TB\",\"isHome\":true},\"17\":{\"abbr\":\"NO\",\"isHome\":true},\"18\":{\"abbr\":\"CAR\",\"isHome\":false},\"2\":{\"abbr\":\"CAR\",\"isHome\":true},\"3\":{\"abbr\":\"GB\",\"isHome\":false},\"4\":{\"abbr\":\"NO\",\"isHome\":false},\"5\":{\"abbr\":\"BAL\",\"isHome\":true},\"6\":{\"abbr\":\"CHI\",\"isHome\":true},\"7\":{\"abbr\":\"SF\",\"isHome\":true},\"8\":{\"abbr\":\"TB\",\"isHome\":false},\"9\":{\"abbr\":\"CIN\",\"isHome\":true}},\"BAL\":{\"1\":{\"abbr\":\"IND\",\"isHome\":false},\"10\":{\"abbr\":\"LAC\",\"isHome\":true},\"11\":{\"abbr\":\"CAR\",\"isHome\":false},\"12\":{\"abbr\":\"HOU\",\"isHome\":false},\"14\":{\"abbr\":\"TB\",\"isHome\":true},\"15\":{\"abbr\":\"PIT\",\"isHome\":false},\"16\":{\"abbr\":\"CLE\",\"isHome\":true},\"17\":{\"abbr\":\"CIN\",\"isHome\":false},\"18\":{\"abbr\":\"PIT\",\"isHome\":true},\"2\":{\"abbr\":\"NO\",\"isHome\":true},\"3\":{\"abbr\":\"DAL\",\"isHome\":false},\"4\":{\"abbr\":\"TEN\",\"isHome\":true},\"5\":{\"abbr\":\"ATL\",\"isHome\":false},\"6\":{\"abbr\":\"CLE\",\"isHome\":false},\"7\":{\"abbr\":\"CIN\",\"isHome\":true},\"8\":{\"abbr\":\"BUF\",\"isHome\":false},\"9\":{\"abbr\":\"JAX\",\"isHome\":true}},\"BUF\":{\"1\":{\"abbr\":\"HOU\",\"isHome\":false},\"10\":{\"abbr\":\"NYJ\",\"isHome\":false},\"11\":{\"abbr\":\"MIA\",\"isHome\":true},\"12\":{\"abbr\":\"KC\",\"isHome\":true},\"13\":{\"abbr\":\"NE\",\"isHome\":false},\"14\":{\"abbr\":\"GB\",\"isHome\":false},\"15\":{\"abbr\":\"CHI\",\"isHome\":true},\"16\":{\"abbr\":\"DEN\",\"isHome\":false},\"17\":{\"abbr\":\"MIA\",\"isHome\":false},\"18\":{\"abbr\":\"NYJ\",\"isHome\":true},\"2\":{\"abbr\":\"DET\",\"isHome\":true},\"3\":{\"abbr\":\"LAC\",\"isHome\":true},\"4\":{\"abbr\":\"NE\",\"isHome\":true},\"5\":{\"abbr\":\"LAR\",\"isHome\":false},\"6\":{\"abbr\":\"LV\",\"isHome\":false},\"8\":{\"abbr\":\"BAL\",\"isHome\":true},\"9\":{\"abbr\":\"MIN\",\"isHome\":false}},\"CAR\":{\"1\":{\"abbr\":\"CHI\",\"isHome\":true},\"10\":{\"abbr\":\"NO\",\"isHome\":false},\"11\":{\"abbr\":\"BAL\",\"isHome\":true},\"12\":{\"abbr\":\"TB\",\"isHome\":false},\"13\":{\"abbr\":\"MIN\",\"isHome\":false},\"14\":{\"abbr\":\"NO\",\"isHome\":true},\"15\":{\"abbr\":\"CIN\",\"isHome\":true},\"16\":{\"abbr\":\"PIT\",\"isHome\":false},\"17\":{\"abbr\":\"SEA\",\"isHome\":true},\"18\":{\"abbr\":\"ATL\",\"isHome\":true},\"2\":{\"abbr\":\"ATL\",\"isHome\":false},\"3\":{\"abbr\":\"CLE\",\"isHome\":false},\"4\":{\"abbr\":\"DET\",\"isHome\":true},\"6\":{\"abbr\":\"PHI\",\"isHome\":false},\"7\":{\"abbr\":\"TB\",\"isHome\":true},\"8\":{\"abbr\":\"GB\",\"isHome\":false},\"9\":{\"abbr\":\"DEN\",\"isHome\":true}},\"CHI\":{\"1\":{\"abbr\":\"CAR\",\"isHome\":false},\"11\":{\"abbr\":\"NO\",\"isHome\":true},\"12\":{\"abbr\":\"DET\",\"isHome\":false},\"13\":{\"abbr\":\"JAX\",\"isHome\":true},\"14\":{\"abbr\":\"MIA\",\"isHome\":false},\"15\":{\"abbr\":\"BUF\",\"isHome\":false},\"16\":{\"abbr\":\"GB\",\"isHome\":true},\"17\":{\"abbr\":\"DET\",\"isHome\":true},\"18\":{\"abbr\":\"MIN\",\"isHome\":false},\"2\":{\"abbr\":\"MIN\",\"isHome\":true},\"3\":{\"abbr\":\"PHI\",\"isHome\":true},\"4\":{\"abbr\":\"NYJ\",\"isHome\":true},\"5\":{\"abbr\":\"GB\",\"isHome\":false},\"6\":{\"abbr\":\"ATL\",\"isHome\":false},\"7\":{\"abbr\":\"NE\",\"isHome\":true},\"8\":{\"abbr\":\"SEA\",\"isHome\":false},\"9\":{\"abbr\":\"TB\",\"isHome\":true}},\"CIN\":{\"1\":{\"abbr\":\"TB\",\"isHome\":true},\"10\":{\"abbr\":\"PIT\",\"isHome\":true},\"11\":{\"abbr\":\"WAS\",\"isHome\":false},\"12\":{\"abbr\":\"NO\",\"isHome\":true},\"13\":{\"abbr\":\"CLE\",\"isHome\":false},\"14\":{\"abbr\":\"KC\",\"isHome\":true},\"15\":{\"abbr\":\"CAR\",\"isHome\":false},\"16\":{\"abbr\":\"IND\",\"isHome\":false},\"17\":{\"abbr\":\"BAL\",\"isHome\":true},\"18\":{\"abbr\":\"CLE\",\"isHome\":true},\"2\":{\"abbr\":\"HOU\",\"isHome\":false},\"3\":{\"abbr\":\"PIT\",\"isHome\":false},\"4\":{\"abbr\":\"JAX\",\"isHome\":true},\"5\":{\"abbr\":\"MIA\",\"isHome\":false},\"7\":{\"abbr\":\"BAL\",\"isHome\":false},\"8\":{\"abbr\":\"TEN\",\"isHome\":true},\"9\":{\"abbr\":\"ATL\",\"isHome\":true}},\"CLE\":{\"1\":{\"abbr\":\"JAX\",\"isHome\":false},\"10\":{\"abbr\":\"HOU\",\"isHome\":true},\"12\":{\"abbr\":\"LV\",\"isHome\":true},\"13\":{\"abbr\":\"CIN\",\"isHome\":true},\"14\":{\"abbr\":\"ATL\",\"isHome\":true},\"15\":{\"abbr\":\"NYG\",\"isHome\":false},\"16\":{\"abbr\":\"BAL\",\"isHome\":false},\"17\":{\"abbr\":\"IND\",\"isHome\":true},\"18\":{\"abbr\":\"CIN\",\"isHome\":false},\"2\":{\"abbr\":\"TB\",\"isHome\":false},\"3\":{\"abbr\":\"CAR\",\"isHome\":true},\"4\":{\"abbr\":\"PIT\",\"isHome\":true},\"5\":{\"abbr\":\"NYJ\",\"isHome\":false},\"6\":{\"abbr\":\"BAL\",\"isHome\":true},\"7\":{\"abbr\":\"TEN\",\"isHome\":false},\"8\":{\"abbr\":\"PIT\",\"isHome\":false},\"9\":{\"abbr\":\"NO\",\"isHome\":false}},\"DAL\":{\"1\":{\"abbr\":\"NYG\",\"isHome\":false},\"10\":{\"abbr\":\"SF\",\"isHome\":true},\"11\":{\"abbr\":\"TEN\",\"isHome\":true},\"12\":{\"abbr\":\"PHI\",\"isHome\":true},\"13\":{\"abbr\":\"SEA\",\"isHome\":false},\"15\":{\"abbr\":\"LAR\",\"isHome\":false},\"16\":{\"abbr\":\"JAX\",\"isHome\":true},\"17\":{\"abbr\":\"NYG\",\"isHome\":true},\"18\":{\"abbr\":\"WAS\",\"isHome\":false},\"2\":{\"abbr\":\"WAS\",\"isHome\":true},\"3\":{\"abbr\":\"BAL\",\"isHome\":true},\"4\":{\"abbr\":\"HOU\",\"isHome\":false},\"5\":{\"abbr\":\"TB\",\"isHome\":true},\"6\":{\"abbr\":\"GB\",\"isHome\":false},\"7\":{\"abbr\":\"PHI\",\"isHome\":false},\"8\":{\"abbr\":\"ARI\",\"isHome\":true},\"9\":{\"abbr\":\"IND\",\"isHome\":false}},\"DEN\":{\"1\":{\"abbr\":\"KC\",\"isHome\":false},\"11\":{\"abbr\":\"LV\",\"isHome\":true},\"12\":{\"abbr\":\"PIT\",\"isHome\":false},\"13\":{\"abbr\":\"MIA\",\"isHome\":true},\"14\":{\"abbr\":\"NYJ\",\"isHome\":false},\"15\":{\"abbr\":\"LV\",\"isHome\":false},\"16\":{\"abbr\":\"BUF\",\"isHome\":true},\"17\":{\"abbr\":\"NE\",\"isHome\":false},\"18\":{\"abbr\":\"LAC\",\"isHome\":true},\"2\":{\"abbr\":\"JAX\",\"isHome\":true},\"3\":{\"abbr\":\"LAR\",\"isHome\":true},\"4\":{\"abbr\":\"SF\",\"isHome\":false},\"5\":{\"abbr\":\"LAC\",\"isHome\":false},\"6\":{\"abbr\":\"SEA\",\"isHome\":true},\"7\":{\"abbr\":\"ARI\",\"isHome\":false},\"8\":{\"abbr\":\"KC\",\"isHome\":true},\"9\":{\"abbr\":\"CAR\",\"isHome\":false}},\"DET\":{\"1\":{\"abbr\":\"NO\",\"isHome\":true},\"10\":{\"abbr\":\"NE\",\"isHome\":true},\"11\":{\"abbr\":\"TB\",\"isHome\":true},\"12\":{\"abbr\":\"CHI\",\"isHome\":true},\"13\":{\"abbr\":\"ATL\",\"isHome\":false},\"14\":{\"abbr\":\"TEN\",\"isHome\":true},\"15\":{\"abbr\":\"MIN\",\"isHome\":false},\"16\":{\"abbr\":\"NYG\",\"isHome\":true},\"17\":{\"abbr\":\"CHI\",\"isHome\":false},\"18\":{\"abbr\":\"GB\",\"isHome\":false},\"2\":{\"abbr\":\"BUF\",\"isHome\":false},\"3\":{\"abbr\":\"NYJ\",\"isHome\":true},\"4\":{\"abbr\":\"CAR\",\"isHome\":false},\"5\":{\"abbr\":\"ARI\",\"isHome\":false},\"7\":{\"abbr\":\"GB\",\"isHome\":true},\"8\":{\"abbr\":\"MIN\",\"isHome\":true},\"9\":{\"abbr\":\"MIA\",\"isHome\":false}},\"GB\":{\"1\":{\"abbr\":\"MIN\",\"isHome\":false},\"10\":{\"abbr\":\"MIN\",\"isHome\":true},\"12\":{\"abbr\":\"LAR\",\"isHome\":false},\"13\":{\"abbr\":\"NO\",\"isHome\":false},\"14\":{\"abbr\":\"BUF\",\"isHome\":true},\"15\":{\"abbr\":\"MIA\",\"isHome\":true},\"16\":{\"abbr\":\"CHI\",\"isHome\":false},\"17\":{\"abbr\":\"HOU\",\"isHome\":true},\"18\":{\"abbr\":\"DET\",\"isHome\":true},\"2\":{\"abbr\":\"NYJ\",\"isHome\":false},\"3\":{\"abbr\":\"ATL\",\"isHome\":true},\"4\":{\"abbr\":\"TB\",\"isHome\":false},\"5\":{\"abbr\":\"CHI\",\"isHome\":true},\"6\":{\"abbr\":\"DAL\",\"isHome\":true},\"7\":{\"abbr\":\"DET\",\"isHome\":false},\"8\":{\"abbr\":\"CAR\",\"isHome\":true},\"9\":{\"abbr\":\"NE\",\"isHome\":false}},\"HOU\":{\"1\":{\"abbr\":\"BUF\",\"isHome\":true},\"10\":{\"abbr\":\"CLE\",\"isHome\":false},\"11\":{\"abbr\":\"IND\",\"isHome\":true},\"12\":{\"abbr\":\"BAL\",\"isHome\":true},\"13\":{\"abbr\":\"PIT\",\"isHome\":false},\"14\":{\"abbr\":\"WAS\",\"isHome\":false},\"15\":{\"abbr\":\"JAX\",\"isHome\":true},\"16\":{\"abbr\":\"PHI\",\"isHome\":false},\"17\":{\"abbr\":\"GB\",\"isHome\":false},\"18\":{\"abbr\":\"TEN\",\"isHome\":true},\"2\":{\"abbr\":\"CIN\",\"isHome\":true},\"3\":{\"abbr\":\"IND\",\"isHome\":false},\"4\":{\"abbr\":\"DAL\",\"isHome\":true},\"5\":{\"abbr\":\"TEN\",\"isHome\":false},\"6\":{\"abbr\":\"JAX\",\"isHome\":false},\"7\":{\"abbr\":\"NYG\",\"isHome\":true},\"9\":{\"abbr\":\"LAC\",\"isHome\":false}},\"IND\":{\"1\":{\"abbr\":\"BAL\",\"isHome\":true},\"10\":{\"abbr\":\"MIA\",\"isHome\":true},\"11\":{\"abbr\":\"HOU\",\"isHome\":false},\"12\":{\"abbr\":\"NYG\",\"isHome\":true},\"14\":{\"abbr\":\"PHI\",\"isHome\":false},\"15\":{\"abbr\":\"TEN\",\"isHome\":false},\"16\":{\"abbr\":\"CIN\",\"isHome\":true},\"17\":{\"abbr\":\"CLE\",\"isHome\":false},\"18\":{\"abbr\":\"JAX\",\"isHome\":true},\"2\":{\"abbr\":\"KC\",\"isHome\":false},\"3\":{\"abbr\":\"HOU\",\"isHome\":true},\"4\":{\"abbr\":\"WAS\",\"isHome\":false},\"5\":{\"abbr\":\"PIT\",\"isHome\":false},\"6\":{\"abbr\":\"TEN\",\"isHome\":true},\"7\":{\"abbr\":\"MIN\",\"isHome\":false},\"8\":{\"abbr\":\"JAX\",\"isHome\":false},\"9\":{\"abbr\":\"DAL\",\"isHome\":true}},\"JAX\":{\"1\":{\"abbr\":\"CLE\",\"isHome\":true},\"10\":{\"abbr\":\"TEN\",\"isHome\":false},\"11\":{\"abbr\":\"NYG\",\"isHome\":false},\"12\":{\"abbr\":\"TEN\",\"isHome\":true},\"13\":{\"abbr\":\"CHI\",\"isHome\":false},\"14\":{\"abbr\":\"PIT\",\"isHome\":true},\"15\":{\"abbr\":\"HOU\",\"isHome\":false},\"16\":{\"abbr\":\"DAL\",\"isHome\":false},\"17\":{\"abbr\":\"WAS\",\"isHome\":true},\"18\":{\"abbr\":\"IND\",\"isHome\":false},\"2\":{\"abbr\":\"DEN\",\"isHome\":false},\"3\":{\"abbr\":\"NE\",\"isHome\":true},\"4\":{\"abbr\":\"CIN\",\"isHome\":false},\"5\":{\"abbr\":\"PHI\",\"isHome\":true},\"6\":{\"abbr\":\"HOU\",\"isHome\":true},\"8\":{\"abbr\":\"IND\",\"isHome\":true},\"9\":{\"abbr\":\"BAL\",\"isHome\":false}},\"KC\":{\"1\":{\"abbr\":\"DEN\",\"isHome\":true},\"10\":{\"abbr\":\"ATL\",\"isHome\":false},\"11\":{\"abbr\":\"ARI\",\"isHome\":true},\"12\":{\"abbr\":\"BUF\",\"isHome\":false},\"13\":{\"abbr\":\"LAR\",\"isHome\":false},\"14\":{\"abbr\":\"CIN\",\"isHome\":false},\"15\":{\"abbr\":\"NE\",\"isHome\":true},\"16\":{\"abbr\":\"SF\",\"isHome\":true},\"17\":{\"abbr\":\"LAC\",\"isHome\":false},\"18\":{\"abbr\":\"LV\",\"isHome\":true},\"2\":{\"abbr\":\"IND\",\"isHome\":true},\"3\":{\"abbr\":\"MIA\",\"isHome\":false},\"4\":{\"abbr\":\"LV\",\"isHome\":false},\"6\":{\"abbr\":\"LAC\",\"isHome\":true},\"7\":{\"abbr\":\"SEA\",\"isHome\":false},\"8\":{\"abbr\":\"DEN\",\"isHome\":false},\"9\":{\"abbr\":\"NYJ\",\"isHome\":true}},\"LAC\":{\"1\":{\"abbr\":\"ARI\",\"isHome\":true},\"10\":{\"abbr\":\"BAL\",\"isHome\":false},\"11\":{\"abbr\":\"NYJ\",\"isHome\":true},\"12\":{\"abbr\":\"NE\",\"isHome\":true},\"13\":{\"abbr\":\"TB\",\"isHome\":false},\"14\":{\"abbr\":\"LV\",\"isHome\":false},\"15\":{\"abbr\":\"SF\",\"isHome\":true},\"16\":{\"abbr\":\"MIA\",\"isHome\":false},\"17\":{\"abbr\":\"KC\",\"isHome\":true},\"18\":{\"abbr\":\"DEN\",\"isHome\":false},\"2\":{\"abbr\":\"LV\",\"isHome\":true},\"3\":{\"abbr\":\"BUF\",\"isHome\":false},\"4\":{\"abbr\":\"SEA\",\"isHome\":false},\"5\":{\"abbr\":\"DEN\",\"isHome\":true},\"6\":{\"abbr\":\"KC\",\"isHome\":false},\"8\":{\"abbr\":\"LAR\",\"isHome\":false},\"9\":{\"abbr\":\"HOU\",\"isHome\":true}},\"LAR\":{\"1\":{\"abbr\":\"SF\",\"isHome\":true},\"10\":{\"abbr\":\"ARI\",\"isHome\":false},\"12\":{\"abbr\":\"GB\",\"isHome\":true},\"13\":{\"abbr\":\"KC\",\"isHome\":true},\"14\":{\"abbr\":\"SF\",\"isHome\":false},\"15\":{\"abbr\":\"DAL\",\"isHome\":true},\"16\":{\"abbr\":\"SEA\",\"isHome\":false},\"17\":{\"abbr\":\"TB\",\"isHome\":false},\"18\":{\"abbr\":\"SEA\",\"isHome\":true},\"2\":{\"abbr\":\"NYG\",\"isHome\":true},\"3\":{\"abbr\":\"DEN\",\"isHome\":false},\"4\":{\"abbr\":\"PHI\",\"isHome\":false},\"5\":{\"abbr\":\"BUF\",\"isHome\":true},\"6\":{\"abbr\":\"ARI\",\"isHome\":true},\"7\":{\"abbr\":\"LV\",\"isHome\":false},\"8\":{\"abbr\":\"LAC\",\"isHome\":true},\"9\":{\"abbr\":\"WAS\",\"isHome\":false}},\"LV\":{\"1\":{\"abbr\":\"MIA\",\"isHome\":true},\"10\":{\"abbr\":\"SEA\",\"isHome\":true},\"11\":{\"abbr\":\"DEN\",\"isHome\":false},\"12\":{\"abbr\":\"CLE\",\"isHome\":false},\"14\":{\"abbr\":\"LAC\",\"isHome\":true},\"15\":{\"abbr\":\"DEN\",\"isHome\":true},\"16\":{\"abbr\":\"TEN\",\"isHome\":true},\"17\":{\"abbr\":\"ARI\",\"isHome\":false},\"18\":{\"abbr\":\"KC\",\"isHome\":false},\"2\":{\"abbr\":\"LAC\",\"isHome\":false},\"3\":{\"abbr\":\"NO\",\"isHome\":false},\"4\":{\"abbr\":\"KC\",\"isHome\":true},\"5\":{\"abbr\":\"NE\",\"isHome\":false},\"6\":{\"abbr\":\"BUF\",\"isHome\":true},\"7\":{\"abbr\":\"LAR\",\"isHome\":true},\"8\":{\"abbr\":\"NYJ\",\"isHome\":false},\"9\":{\"abbr\":\"SF\",\"isHome\":false}},\"MIA\":{\"1\":{\"abbr\":\"LV\",\"isHome\":false},\"10\":{\"abbr\":\"IND\",\"isHome\":false},\"11\":{\"abbr\":\"BUF\",\"isHome\":false},\"12\":{\"abbr\":\"NYJ\",\"isHome\":true},\"13\":{\"abbr\":\"DEN\",\"isHome\":false},\"14\":{\"abbr\":\"CHI\",\"isHome\":true},\"15\":{\"abbr\":\"GB\",\"isHome\":false},\"16\":{\"abbr\":\"LAC\",\"isHome\":true},\"17\":{\"abbr\":\"BUF\",\"isHome\":true},\"18\":{\"abbr\":\"NE\",\"isHome\":false},\"2\":{\"abbr\":\"SF\",\"isHome\":false},\"3\":{\"abbr\":\"KC\",\"isHome\":true},\"4\":{\"abbr\":\"MIN\",\"isHome\":false},\"5\":{\"abbr\":\"CIN\",\"isHome\":true},\"7\":{\"abbr\":\"NYJ\",\"isHome\":false},\"8\":{\"abbr\":\"NE\",\"isHome\":true},\"9\":{\"abbr\":\"DET\",\"isHome\":true}},\"MIN\":{\"1\":{\"abbr\":\"GB\",\"isHome\":true},\"10\":{\"abbr\":\"GB\",\"isHome\":false},\"11\":{\"abbr\":\"SF\",\"isHome\":false},\"12\":{\"abbr\":\"ATL\",\"isHome\":true},\"13\":{\"abbr\":\"CAR\",\"isHome\":true},\"14\":{\"abbr\":\"NE\",\"isHome\":false},\"15\":{\"abbr\":\"DET\",\"isHome\":true},\"16\":{\"abbr\":\"WAS\",\"isHome\":true},\"17\":{\"abbr\":\"NYJ\",\"isHome\":false},\"18\":{\"abbr\":\"CHI\",\"isHome\":true},\"2\":{\"abbr\":\"CHI\",\"isHome\":false},\"3\":{\"abbr\":\"TB\",\"isHome\":false},\"4\":{\"abbr\":\"MIA\",\"isHome\":true},\"5\":{\"abbr\":\"NO\",\"isHome\":false},\"7\":{\"abbr\":\"IND\",\"isHome\":true},\"8\":{\"abbr\":\"DET\",\"isHome\":false},\"9\":{\"abbr\":\"BUF\",\"isHome\":true}},\"NE\":{\"1\":{\"abbr\":\"SEA\",\"isHome\":false},\"10\":{\"abbr\":\"DET\",\"isHome\":false},\"12\":{\"abbr\":\"LAC\",\"isHome\":false},\"13\":{\"abbr\":\"BUF\",\"isHome\":true},\"14\":{\"abbr\":\"MIN\",\"isHome\":true},\"15\":{\"abbr\":\"KC\",\"isHome\":false},\"16\":{\"abbr\":\"NYJ\",\"isHome\":false},\"17\":{\"abbr\":\"DEN\",\"isHome\":true},\"18\":{\"abbr\":\"MIA\",\"isHome\":true},\"2\":{\"abbr\":\"PIT\",\"isHome\":true},\"3\":{\"abbr\":\"JAX\",\"isHome\":false},\"4\":{\"abbr\":\"BUF\",\"isHome\":false},\"5\":{\"abbr\":\"LV\",\"isHome\":true},\"6\":{\"abbr\":\"NYJ\",\"isHome\":true},\"7\":{\"abbr\":\"CHI\",\"isHome\":false},\"8\":{\"abbr\":\"MIA\",\"isHome\":false},\"9\":{\"abbr\":\"GB\",\"isHome\":true}},\"NO\":{\"1\":{\"abbr\":\"DET\",\"isHome\":false},\"10\":{\"abbr\":\"CAR\",\"isHome\":true},\"11\":{\"abbr\":\"CHI\",\"isHome\":false},\"12\":{\"abbr\":\"CIN\",\"isHome\":false},\"13\":{\"abbr\":\"GB\",\"isHome\":true},\"14\":{\"abbr\":\"CAR\",\"isHome\":false},\"15\":{\"abbr\":\"TB\",\"isHome\":false},\"16\":{\"abbr\":\"ARI\",\"isHome\":true},\"17\":{\"abbr\":\"ATL\",\"isHome\":false},\"18\":{\"abbr\":\"TB\",\"isHome\":true},\"2\":{\"abbr\":\"BAL\",\"isHome\":false},\"3\":{\"abbr\":\"LV\",\"isHome\":true},\"4\":{\"abbr\":\"ATL\",\"isHome\":true},\"5\":{\"abbr\":\"MIN\",\"isHome\":true},\"6\":{\"abbr\":\"NYG\",\"isHome\":false},\"7\":{\"abbr\":\"PIT\",\"isHome\":true},\"9\":{\"abbr\":\"CLE\",\"isHome\":true}},\"NYG\":{\"1\":{\"abbr\":\"DAL\",\"isHome\":true},\"10\":{\"abbr\":\"WAS\",\"isHome\":true},\"11\":{\"abbr\":\"JAX\",\"isHome\":true},\"12\":{\"abbr\":\"IND\",\"isHome\":false},\"13\":{\"abbr\":\"SF\",\"isHome\":true},\"14\":{\"abbr\":\"SEA\",\"isHome\":false},\"15\":{\"abbr\":\"CLE\",\"isHome\":true},\"16\":{\"abbr\":\"DET\",\"isHome\":false},\"17\":{\"abbr\":\"DAL\",\"isHome\":false},\"18\":{\"abbr\":\"PHI\",\"isHome\":true},\"2\":{\"abbr\":\"LAR\",\"isHome\":false},\"3\":{\"abbr\":\"TEN\",\"isHome\":true},\"4\":{\"abbr\":\"ARI\",\"isHome\":true},\"5\":{\"abbr\":\"WAS\",\"isHome\":false},\"6\":{\"abbr\":\"NO\",\"isHome\":true},\"7\":{\"abbr\":\"HOU\",\"isHome\":false},\"9\":{\"abbr\":\"PHI\",\"isHome\":false}},\"NYJ\":{\"1\":{\"abbr\":\"TEN\",\"isHome\":false},\"10\":{\"abbr\":\"BUF\",\"isHome\":true},\"11\":{\"abbr\":\"LAC\",\"isHome\":false},\"12\":{\"abbr\":\"MIA\",\"isHome\":false},\"14\":{\"abbr\":\"DEN\",\"isHome\":true},\"15\":{\"abbr\":\"ARI\",\"isHome\":false},\"16\":{\"abbr\":\"NE\",\"isHome\":true},\"17\":{\"abbr\":\"MIN\",\"isHome\":true},\"18\":{\"abbr\":\"BUF\",\"isHome\":false},\"2\":{\"abbr\":\"GB\",\"isHome\":true},\"3\":{\"abbr\":\"DET\",\"isHome\":false},\"4\":{\"abbr\":\"CHI\",\"isHome\":false},\"5\":{\"abbr\":\"CLE\",\"isHome\":true},\"6\":{\"abbr\":\"NE\",\"isHome\":false},\"7\":{\"abbr\":\"MIA\",\"isHome\":true},\"8\":{\"abbr\":\"LV\",\"isHome\":true},\"9\":{\"abbr\":\"KC\",\"isHome\":false}},\"PHI\":{\"1\":{\"abbr\":\"WAS\",\"isHome\":true},\"11\":{\"abbr\":\"PIT\",\"isHome\":true},\"12\":{\"abbr\":\"DAL\",\"isHome\":false},\"13\":{\"abbr\":\"ARI\",\"isHome\":false},\"14\":{\"abbr\":\"IND\",\"isHome\":true},\"15\":{\"abbr\":\"SEA\",\"isHome\":true},\"16\":{\"abbr\":\"HOU\",\"isHome\":true},\"17\":{\"abbr\":\"SF\",\"isHome\":false},\"18\":{\"abbr\":\"NYG\",\"isHome\":false},\"2\":{\"abbr\":\"TEN\",\"isHome\":false},\"3\":{\"abbr\":\"CHI\",\"isHome\":false},\"4\":{\"abbr\":\"LAR\",\"isHome\":true},\"5\":{\"abbr\":\"JAX\",\"isHome\":false},\"6\":{\"abbr\":\"CAR\",\"isHome\":true},\"7\":{\"abbr\":\"DAL\",\"isHome\":true},\"8\":{\"abbr\":\"WAS\",\"isHome\":false},\"9\":{\"abbr\":\"NYG\",\"isHome\":true}},\"PIT\":{\"1\":{\"abbr\":\"ATL\",\"isHome\":true},\"10\":{\"abbr\":\"CIN\",\"isHome\":false},\"11\":{\"abbr\":\"PHI\",\"isHome\":false},\"12\":{\"abbr\":\"DEN\",\"isHome\":true},\"13\":{\"abbr\":\"HOU\",\"isHome\":true},\"14\":{\"abbr\":\"JAX\",\"isHome\":false},\"15\":{\"abbr\":\"BAL\",\"isHome\":true},\"16\":{\"abbr\":\"CAR\",\"isHome\":true},\"17\":{\"abbr\":\"TEN\",\"isHome\":false},\"18\":{\"abbr\":\"BAL\",\"isHome\":false},\"2\":{\"abbr\":\"NE\",\"isHome\":false},\"3\":{\"abbr\":\"CIN\",\"isHome\":true},\"4\":{\"abbr\":\"CLE\",\"isHome\":false},\"5\":{\"abbr\":\"IND\",\"isHome\":true},\"6\":{\"abbr\":\"TB\",\"isHome\":false},\"7\":{\"abbr\":\"NO\",\"isHome\":false},\"8\":{\"abbr\":\"CLE\",\"isHome\":true}},\"SEA\":{\"1\":{\"abbr\":\"NE\",\"isHome\":true},\"10\":{\"abbr\":\"LV\",\"isHome\":false},\"12\":{\"abbr\":\"SF\",\"isHome\":false},\"13\":{\"abbr\":\"DAL\",\"isHome\":true},\"14\":{\"abbr\":\"NYG\",\"isHome\":true},\"15\":{\"abbr\":\"PHI\",\"isHome\":false},\"16\":{\"abbr\":\"LAR\",\"isHome\":true},\"17\":{\"abbr\":\"CAR\",\"isHome\":false},\"18\":{\"abbr\":\"LAR\",\"isHome\":false},\"2\":{\"abbr\":\"ARI\",\"isHome\":false},\"3\":{\"abbr\":\"WAS\",\"isHome\":false},\"4\":{\"abbr\":\"LAC\",\"isHome\":true},\"5\":{\"abbr\":\"SF\",\"isHome\":true},\"6\":{\"abbr\":\"DEN\",\"isHome\":false},\"7\":{\"abbr\":\"KC\",\"isHome\":true},\"8\":{\"abbr\":\"CHI\",\"isHome\":true},\"9\":{\"abbr\":\"ARI\",\"isHome\":true}},\"SF\":{\"1\":{\"abbr\":\"LAR\",\"isHome\":false},\"10\":{\"abbr\":\"DAL\",\"isHome\":false},\"11\":{\"abbr\":\"MIN\",\"isHome\":true},\"12\":{\"abbr\":\"SEA\",\"isHome\":true},\"13\":{\"abbr\":\"NYG\",\"isHome\":false},\"14\":{\"abbr\":\"LAR\",\"isHome\":true},\"15\":{\"abbr\":\"LAC\",\"isHome\":false},\"16\":{\"abbr\":\"KC\",\"isHome\":false},\"17\":{\"abbr\":\"PHI\",\"isHome\":true},\"18\":{\"abbr\":\"ARI\",\"isHome\":false},\"2\":{\"abbr\":\"MIA\",\"isHome\":true},\"3\":{\"abbr\":\"ARI\",\"isHome\":true},\"4\":{\"abbr\":\"DEN\",\"isHome\":true},\"5\":{\"abbr\":\"SEA\",\"isHome\":false},\"6\":{\"abbr\":\"WAS\",\"isHome\":true},\"7\":{\"abbr\":\"ATL\",\"isHome\":false},\"9\":{\"abbr\":\"LV\",\"isHome\":true}},\"TB\":{\"1\":{\"abbr\":\"CIN\",\"isHome\":false},\"11\":{\"abbr\":\"DET\",\"isHome\":false},\"12\":{\"abbr\":\"CAR\",\"isHome\":true},\"13\":{\"abbr\":\"LAC\",\"isHome\":true},\"14\":{\"abbr\":\"BAL\",\"isHome\":false},\"15\":{\"abbr\":\"NO\",\"isHome\":true},\"16\":{\"abbr\":\"ATL\",\"isHome\":false},\"17\":{\"abbr\":\"LAR\",\"isHome\":true},\"18\":{\"abbr\":\"NO\",\"isHome\":false},\"2\":{\"abbr\":\"CLE\",\"isHome\":true},\"3\":{\"abbr\":\"MIN\",\"isHome\":true},\"4\":{\"abbr\":\"GB\",\"isHome\":true},\"5\":{\"abbr\":\"DAL\",\"isHome\":false},\"6\":{\"abbr\":\"PIT\",\"isHome\":true},\"7\":{\"abbr\":\"CAR\",\"isHome\":false},\"8\":{\"abbr\":\"ATL\",\"isHome\":true},\"9\":{\"abbr\":\"CHI\",\"isHome\":false}},\"TEN\":{\"1\":{\"abbr\":\"NYJ\",\"isHome\":true},\"10\":{\"abbr\":\"JAX\",\"isHome\":true},\"11\":{\"abbr\":\"DAL\",\"isHome\":false},\"12\":{\"abbr\":\"JAX\",\"isHome\":false},\"13\":{\"abbr\":\"WAS\",\"isHome\":true},\"14\":{\"abbr\":\"DET\",\"isHome\":false},\"15\":{\"abbr\":\"IND\",\"isHome\":true},\"16\":{\"abbr\":\"LV\",\"isHome\":false},\"17\":{\"abbr\":\"PIT\",\"isHome\":true},\"18\":{\"abbr\":\"HOU\",\"isHome\":false},\"2\":{\"abbr\":\"PHI\",\"isHome\":true},\"3\":{\"abbr\":\"NYG\",\"isHome\":false},\"4\":{\"abbr\":\"BAL\",\"isHome\":false},\"5\":{\"abbr\":\"HOU\",\"isHome\":true},\"6\":{\"abbr\":\"IND\",\"isHome\":false},\"7\":{\"abbr\":\"CLE\",\"isHome\":true},\"8\":{\"abbr\":\"CIN\",\"isHome\":false}},\"WAS\":{\"1\":{\"abbr\":\"PHI\",\"isHome\":false},\"10\":{\"abbr\":\"NYG\",\"isHome\":false},\"11\":{\"abbr\":\"CIN\",\"isHome\":true},\"12\":{\"abbr\":\"ARI\",\"isHome\":false},\"13\":{\"abbr\":\"TEN\",\"isHome\":false},\"14\":{\"abbr\":\"HOU\",\"isHome\":true},\"15\":{\"abbr\":\"ATL\",\"isHome\":true},\"16\":{\"abbr\":\"MIN\",\"isHome\":false},\"17\":{\"abbr\":\"JAX\",\"isHome\":false},\"18\":{\"abbr\":\"DAL\",\"isHome\":true},\"2\":{\"abbr\":\"DAL\",\"isHome\":false},\"3\":{\"abbr\":\"SEA\",\"isHome\":true},\"4\":{\"abbr\":\"IND\",\"isHome\":true},\"5\":{\"abbr\":\"NYG\",\"isHome\":true},\"6\":{\"abbr\":\"SF\",\"isHome\":false},\"8\":{\"abbr\":\"PHI\",\"isHome\":true},\"9\":{\"abbr\":\"LAR\",\"isHome\":true}}}");
}),
"[project]/web/lib/slug.js [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/** URL slugs for player pages: "John Metchie" -> "john-metchie". */ __turbopack_context__.s([
    "slugify",
    ()=>slugify
]);
function slugify(name) {
    return (name || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__0qtcyyp._.js.map