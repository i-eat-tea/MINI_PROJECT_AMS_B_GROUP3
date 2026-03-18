import { useState, useMemo } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  LineChart, Line, PieChart, Pie, Cell, ResponsiveContainer,
  AreaChart, Area,
} from "recharts";

// ── DATA ─────────────────────────────────────────────────────────────────────
const overviewRaw = [{"province":"Banteay Meanchey","year":2018,"schools":818,"classes":4598,"enrollment":152590,"enrollF":76099,"repeaters":4051,"repeatersF":1371,"teachStaff":4782,"teachF":2440,"nonTeach":888,"nonTeachF":210},{"province":"Battambang","year":2018,"schools":1133,"classes":7494,"enrollment":253481,"enrollF":125579,"repeaters":12244,"repeatersF":4362,"teachStaff":6946,"teachF":4165,"nonTeach":1811,"nonTeachF":672},{"province":"Kampong Cham","year":2018,"schools":804,"classes":5846,"enrollment":221707,"enrollF":110363,"repeaters":14544,"repeatersF":5235,"teachStaff":5835,"teachF":3390,"nonTeach":1695,"nonTeachF":659},{"province":"Kampong Chhnang","year":2018,"schools":466,"classes":3220,"enrollment":118144,"enrollF":59641,"repeaters":5080,"repeatersF":1676,"teachStaff":3498,"teachF":1682,"nonTeach":700,"nonTeachF":188},{"province":"Kampong Speu","year":2018,"schools":603,"classes":4162,"enrollment":170222,"enrollF":83971,"repeaters":5931,"repeatersF":2157,"teachStaff":4471,"teachF":1957,"nonTeach":742,"nonTeachF":129},{"province":"Kampong Thom","year":2018,"schools":782,"classes":4593,"enrollment":156111,"enrollF":79001,"repeaters":8302,"repeatersF":3087,"teachStaff":4435,"teachF":2429,"nonTeach":731,"nonTeachF":179},{"province":"Kampot","year":2018,"schools":608,"classes":3699,"enrollment":129794,"enrollF":63442,"repeaters":4229,"repeatersF":1366,"teachStaff":4747,"teachF":2325,"nonTeach":938,"nonTeachF":189},{"province":"Kandal","year":2018,"schools":748,"classes":6547,"enrollment":251350,"enrollF":123416,"repeaters":14523,"repeatersF":5120,"teachStaff":7246,"teachF":4002,"nonTeach":1482,"nonTeachF":412},{"province":"Kep","year":2018,"schools":50,"classes":272,"enrollment":8689,"enrollF":4340,"repeaters":324,"repeatersF":120,"teachStaff":455,"teachF":239,"nonTeach":92,"nonTeachF":15},{"province":"Koh Kong","year":2018,"schools":218,"classes":1113,"enrollment":26513,"enrollF":12817,"repeaters":737,"repeatersF":274,"teachStaff":1074,"teachF":484,"nonTeach":164,"nonTeachF":45},{"province":"Kratie","year":2018,"schools":418,"classes":2736,"enrollment":86175,"enrollF":42715,"repeaters":5378,"repeatersF":2021,"teachStaff":2550,"teachF":1585,"nonTeach":367,"nonTeachF":122},{"province":"Mondul Kiri","year":2018,"schools":126,"classes":783,"enrollment":20253,"enrollF":10194,"repeaters":784,"repeatersF":293,"teachStaff":812,"teachF":380,"nonTeach":46,"nonTeachF":9},{"province":"Otdar Meanchey","year":2018,"schools":358,"classes":1934,"enrollment":54721,"enrollF":26651,"repeaters":3337,"repeatersF":1192,"teachStaff":1525,"teachF":679,"nonTeach":302,"nonTeachF":65},{"province":"Pailin","year":2018,"schools":82,"classes":501,"enrollment":16097,"enrollF":7978,"repeaters":831,"repeatersF":260,"teachStaff":625,"teachF":315,"nonTeach":76,"nonTeachF":22},{"province":"Phnom Penh","year":2018,"schools":376,"classes":5609,"enrollment":236464,"enrollF":114772,"repeaters":6597,"repeatersF":2159,"teachStaff":9841,"teachF":5742,"nonTeach":1042,"nonTeachF":407},{"province":"Preah Sihanouk","year":2018,"schools":156,"classes":1187,"enrollment":41484,"enrollF":20519,"repeaters":1169,"repeatersF":388,"teachStaff":1598,"teachF":775,"nonTeach":239,"nonTeachF":74},{"province":"Preah Vihear","year":2018,"schools":401,"classes":2038,"enrollment":55386,"enrollF":27860,"repeaters":3251,"repeatersF":1309,"teachStaff":1999,"teachF":1002,"nonTeach":266,"nonTeachF":72},{"province":"Prey Veng","year":2018,"schools":1035,"classes":6615,"enrollment":234696,"enrollF":114530,"repeaters":10825,"repeatersF":3840,"teachStaff":5736,"teachF":2709,"nonTeach":1800,"nonTeachF":455},{"province":"Pursat","year":2018,"schools":537,"classes":3207,"enrollment":104684,"enrollF":52250,"repeaters":5820,"repeatersF":2237,"teachStaff":3156,"teachF":1520,"nonTeach":610,"nonTeachF":161},{"province":"Ratanak Kiri","year":2018,"schools":303,"classes":1703,"enrollment":54148,"enrollF":26126,"repeaters":1862,"repeatersF":760,"teachStaff":1275,"teachF":590,"nonTeach":123,"nonTeachF":30},{"province":"Siemreap","year":2018,"schools":1067,"classes":6918,"enrollment":265926,"enrollF":133764,"repeaters":14357,"repeatersF":5036,"teachStaff":5950,"teachF":3699,"nonTeach":1446,"nonTeachF":536},{"province":"Stung Treng","year":2018,"schools":218,"classes":1359,"enrollment":33974,"enrollF":16838,"repeaters":2764,"repeatersF":1198,"teachStaff":1217,"teachF":657,"nonTeach":169,"nonTeachF":58},{"province":"Svay Rieng","year":2018,"schools":508,"classes":3344,"enrollment":118078,"enrollF":58287,"repeaters":3708,"repeatersF":1253,"teachStaff":3688,"teachF":1394,"nonTeach":929,"nonTeachF":208},{"province":"Takeo","year":2018,"schools":782,"classes":5777,"enrollment":206362,"enrollF":100713,"repeaters":9407,"repeatersF":3205,"teachStaff":6485,"teachF":2627,"nonTeach":1696,"nonTeachF":391},{"province":"Tbaung Khmum","year":2018,"schools":703,"classes":4642,"enrollment":172123,"enrollF":85405,"repeaters":7966,"repeatersF":3018,"teachStaff":3757,"teachF":2023,"nonTeach":712,"nonTeachF":223},{"province":"Banteay Meanchey","year":2019,"schools":818,"classes":4667,"enrollment":156200,"enrollF":78140,"repeaters":4292,"repeatersF":1427,"teachStaff":4834,"teachF":2516,"nonTeach":894,"nonTeachF":216},{"province":"Battambang","year":2019,"schools":1147,"classes":7694,"enrollment":255364,"enrollF":126697,"repeaters":11683,"repeatersF":4157,"teachStaff":6851,"teachF":4128,"nonTeach":1686,"nonTeachF":632},{"province":"Kampong Cham","year":2019,"schools":816,"classes":5905,"enrollment":221352,"enrollF":110434,"repeaters":13360,"repeatersF":4715,"teachStaff":5779,"teachF":3352,"nonTeach":1743,"nonTeachF":684},{"province":"Kampong Chhnang","year":2019,"schools":469,"classes":3204,"enrollment":117422,"enrollF":59488,"repeaters":4960,"repeatersF":1671,"teachStaff":3567,"teachF":1727,"nonTeach":675,"nonTeachF":175},{"province":"Kampong Speu","year":2019,"schools":619,"classes":4144,"enrollment":168939,"enrollF":83978,"repeaters":6101,"repeatersF":2240,"teachStaff":4390,"teachF":1939,"nonTeach":793,"nonTeachF":142},{"province":"Kampong Thom","year":2019,"schools":789,"classes":4575,"enrollment":156323,"enrollF":79333,"repeaters":8286,"repeatersF":2979,"teachStaff":4398,"teachF":2444,"nonTeach":774,"nonTeachF":192},{"province":"Kampot","year":2019,"schools":611,"classes":3862,"enrollment":127197,"enrollF":62568,"repeaters":4873,"repeatersF":1584,"teachStaff":4802,"teachF":2378,"nonTeach":944,"nonTeachF":199},{"province":"Kandal","year":2019,"schools":752,"classes":6609,"enrollment":254957,"enrollF":125751,"repeaters":14221,"repeatersF":4896,"teachStaff":7298,"teachF":4050,"nonTeach":1461,"nonTeachF":391},{"province":"Kep","year":2019,"schools":50,"classes":276,"enrollment":8559,"enrollF":4280,"repeaters":569,"repeatersF":173,"teachStaff":456,"teachF":239,"nonTeach":93,"nonTeachF":20},{"province":"Koh Kong","year":2019,"schools":219,"classes":1101,"enrollment":26566,"enrollF":13043,"repeaters":894,"repeatersF":323,"teachStaff":1097,"teachF":503,"nonTeach":162,"nonTeachF":41},{"province":"Kratie","year":2019,"schools":441,"classes":2781,"enrollment":87204,"enrollF":43228,"repeaters":5292,"repeatersF":1975,"teachStaff":2577,"teachF":1623,"nonTeach":372,"nonTeachF":132},{"province":"Mondul Kiri","year":2019,"schools":127,"classes":801,"enrollment":20688,"enrollF":10487,"repeaters":704,"repeatersF":279,"teachStaff":839,"teachF":408,"nonTeach":53,"nonTeachF":11},{"province":"Otdar Meanchey","year":2019,"schools":359,"classes":1957,"enrollment":55614,"enrollF":27193,"repeaters":3495,"repeatersF":1227,"teachStaff":1561,"teachF":721,"nonTeach":318,"nonTeachF":73},{"province":"Pailin","year":2019,"schools":81,"classes":512,"enrollment":16597,"enrollF":8233,"repeaters":745,"repeatersF":254,"teachStaff":636,"teachF":341,"nonTeach":81,"nonTeachF":22},{"province":"Phnom Penh","year":2019,"schools":374,"classes":5501,"enrollment":239768,"enrollF":116931,"repeaters":7094,"repeatersF":2424,"teachStaff":9445,"teachF":5506,"nonTeach":1133,"nonTeachF":439},{"province":"Preah Sihanouk","year":2019,"schools":157,"classes":1200,"enrollment":41390,"enrollF":20581,"repeaters":1717,"repeatersF":606,"teachStaff":1570,"teachF":781,"nonTeach":232,"nonTeachF":75},{"province":"Preah Vihear","year":2019,"schools":407,"classes":2132,"enrollment":57474,"enrollF":29080,"repeaters":3493,"repeatersF":1295,"teachStaff":2041,"teachF":1061,"nonTeach":321,"nonTeachF":88},{"province":"Prey Veng","year":2019,"schools":1057,"classes":6676,"enrollment":236800,"enrollF":115758,"repeaters":10644,"repeatersF":3670,"teachStaff":5648,"teachF":2699,"nonTeach":1863,"nonTeachF":450},{"province":"Pursat","year":2019,"schools":543,"classes":3281,"enrollment":107028,"enrollF":53680,"repeaters":5715,"repeatersF":2194,"teachStaff":3138,"teachF":1540,"nonTeach":679,"nonTeachF":191},{"province":"Ratanak Kiri","year":2019,"schools":311,"classes":1856,"enrollment":55611,"enrollF":27048,"repeaters":1808,"repeatersF":717,"teachStaff":1316,"teachF":624,"nonTeach":125,"nonTeachF":33},{"province":"Siemreap","year":2019,"schools":1077,"classes":7066,"enrollment":271653,"enrollF":137200,"repeaters":14290,"repeatersF":4801,"teachStaff":5769,"teachF":3579,"nonTeach":1809,"nonTeachF":792},{"province":"Stung Treng","year":2019,"schools":246,"classes":1454,"enrollment":35518,"enrollF":17611,"repeaters":2686,"repeatersF":1125,"teachStaff":1321,"teachF":740,"nonTeach":146,"nonTeachF":46},{"province":"Svay Rieng","year":2019,"schools":509,"classes":3613,"enrollment":119268,"enrollF":59229,"repeaters":3727,"repeatersF":1205,"teachStaff":3694,"teachF":1423,"nonTeach":933,"nonTeachF":211},{"province":"Takeo","year":2019,"schools":793,"classes":5706,"enrollment":201228,"enrollF":99349,"repeaters":12020,"repeatersF":3922,"teachStaff":6473,"teachF":2652,"nonTeach":1724,"nonTeachF":402},{"province":"Tbaung Khmum","year":2019,"schools":710,"classes":4686,"enrollment":171565,"enrollF":85727,"repeaters":8088,"repeatersF":2968,"teachStaff":3725,"teachF":2068,"nonTeach":848,"nonTeachF":246},{"province":"Banteay Meanchey","year":2020,"schools":822,"classes":4882,"enrollment":164159,"enrollF":82496,"repeaters":5391,"repeatersF":1961,"teachStaff":4766,"teachF":2503,"nonTeach":938,"nonTeachF":243},{"province":"Battambang","year":2020,"schools":1170,"classes":7827,"enrollment":257116,"enrollF":128312,"repeaters":13223,"repeatersF":5076,"teachStaff":7099,"teachF":4290,"nonTeach":1758,"nonTeachF":670},{"province":"Kampong Cham","year":2020,"schools":820,"classes":6116,"enrollment":223361,"enrollF":118213,"repeaters":14549,"repeatersF":5407,"teachStaff":5840,"teachF":3411,"nonTeach":1779,"nonTeachF":722},{"province":"Kampong Chhnang","year":2020,"schools":472,"classes":3307,"enrollment":118383,"enrollF":61090,"repeaters":6480,"repeatersF":2210,"teachStaff":3586,"teachF":1776,"nonTeach":740,"nonTeachF":213},{"province":"Kampong Speu","year":2020,"schools":631,"classes":4182,"enrollment":165484,"enrollF":81809,"repeaters":6624,"repeatersF":2620,"teachStaff":4308,"teachF":1970,"nonTeach":871,"nonTeachF":177},{"province":"Kampong Thom","year":2020,"schools":800,"classes":4920,"enrollment":158695,"enrollF":84240,"repeaters":8224,"repeatersF":3068,"teachStaff":4463,"teachF":2526,"nonTeach":828,"nonTeachF":218},{"province":"Kampot","year":2020,"schools":612,"classes":4710,"enrollment":125456,"enrollF":61766,"repeaters":4613,"repeatersF":1626,"teachStaff":4740,"teachF":2374,"nonTeach":998,"nonTeachF":226},{"province":"Kandal","year":2020,"schools":761,"classes":6810,"enrollment":263786,"enrollF":130356,"repeaters":19661,"repeatersF":7286,"teachStaff":7299,"teachF":4114,"nonTeach":1516,"nonTeachF":402},{"province":"Kep","year":2020,"schools":50,"classes":300,"enrollment":9014,"enrollF":4477,"repeaters":350,"repeatersF":111,"teachStaff":476,"teachF":258,"nonTeach":97,"nonTeachF":19},{"province":"Koh Kong","year":2020,"schools":223,"classes":1204,"enrollment":28113,"enrollF":13868,"repeaters":995,"repeatersF":376,"teachStaff":1199,"teachF":578,"nonTeach":186,"nonTeachF":53},{"province":"Kratie","year":2020,"schools":446,"classes":2993,"enrollment":89547,"enrollF":47017,"repeaters":6580,"repeatersF":2591,"teachStaff":2696,"teachF":1706,"nonTeach":404,"nonTeachF":144},{"province":"Mondul Kiri","year":2020,"schools":132,"classes":862,"enrollment":22045,"enrollF":11465,"repeaters":1161,"repeatersF":439,"teachStaff":937,"teachF":484,"nonTeach":68,"nonTeachF":12},{"province":"Otdar Meanchey","year":2020,"schools":366,"classes":2090,"enrollment":57618,"enrollF":28479,"repeaters":3547,"repeatersF":1318,"teachStaff":1641,"teachF":767,"nonTeach":349,"nonTeachF":87},{"province":"Pailin","year":2020,"schools":82,"classes":540,"enrollment":16283,"enrollF":8278,"repeaters":947,"repeatersF":375,"teachStaff":669,"teachF":355,"nonTeach":95,"nonTeachF":30},{"province":"Phnom Penh","year":2020,"schools":380,"classes":5707,"enrollment":245356,"enrollF":119102,"repeaters":9470,"repeatersF":3699,"teachStaff":9242,"teachF":5332,"nonTeach":1170,"nonTeachF":453},{"province":"Preah Sihanouk","year":2020,"schools":159,"classes":1252,"enrollment":44262,"enrollF":21758,"repeaters":2592,"repeatersF":998,"teachStaff":1658,"teachF":856,"nonTeach":272,"nonTeachF":81},{"province":"Preah Vihear","year":2020,"schools":411,"classes":2228,"enrollment":58449,"enrollF":29838,"repeaters":4311,"repeatersF":1737,"teachStaff":2178,"teachF":1139,"nonTeach":350,"nonTeachF":109},{"province":"Prey Veng","year":2020,"schools":1071,"classes":6884,"enrollment":241931,"enrollF":118122,"repeaters":12332,"repeatersF":4439,"teachStaff":5860,"teachF":2826,"nonTeach":1926,"nonTeachF":504},{"province":"Pursat","year":2020,"schools":551,"classes":3355,"enrollment":111387,"enrollF":58990,"repeaters":6787,"repeatersF":2646,"teachStaff":3140,"teachF":1585,"nonTeach":735,"nonTeachF":205},{"province":"Ratanak Kiri","year":2020,"schools":328,"classes":1967,"enrollment":56346,"enrollF":28110,"repeaters":2294,"repeatersF":934,"teachStaff":1430,"teachF":699,"nonTeach":142,"nonTeachF":43},{"province":"Siemreap","year":2020,"schools":1109,"classes":7625,"enrollment":278744,"enrollF":143448,"repeaters":17570,"repeatersF":6287,"teachStaff":5943,"teachF":3759,"nonTeach":1758,"nonTeachF":734},{"province":"Stung Treng","year":2020,"schools":259,"classes":1782,"enrollment":38032,"enrollF":19508,"repeaters":3576,"repeatersF":1532,"teachStaff":1411,"teachF":787,"nonTeach":194,"nonTeachF":57},{"province":"Svay Rieng","year":2020,"schools":511,"classes":3568,"enrollment":121308,"enrollF":59173,"repeaters":4560,"repeatersF":1574,"teachStaff":3747,"teachF":1499,"nonTeach":971,"nonTeachF":221},{"province":"Takeo","year":2020,"schools":802,"classes":5907,"enrollment":200404,"enrollF":98718,"repeaters":9808,"repeatersF":3522,"teachStaff":6486,"teachF":2754,"nonTeach":1771,"nonTeachF":393},{"province":"Tbaung Khmum","year":2020,"schools":723,"classes":4891,"enrollment":170498,"enrollF":85439,"repeaters":10073,"repeatersF":3828,"teachStaff":3904,"teachF":2197,"nonTeach":915,"nonTeachF":271}];

const nationalTotals = [{"year":"2018–19","schools":13300,"enrollment":3189172,"enrollF":1577271,"repeaters":148021,"teachStaff":93703,"teachF":48810,"nonTeach":19066},{"year":"2019–20","schools":13482,"enrollment":3210285,"enrollF":1595047,"repeaters":150757,"teachStaff":93225,"teachF":49042,"nonTeach":19862},{"year":"2020–21","schools":13681,"enrollment":3277076,"enrollF":1652532,"repeaters":175718,"teachStaff":94718,"teachF":50545,"nonTeach":20831}];

const staffQual = [{"year":2018,"level":"Primary","total":1651,"noPed":30},{"year":2018,"level":"L.Secondary","total":17217,"noPed":131},{"year":2018,"level":"U.Secondary","total":50808,"noPed":283},{"year":2018,"level":"Graduate","total":22657,"noPed":181},{"year":2018,"level":"PostGrad","total":1377,"noPed":10},{"year":2018,"level":"PhD","total":10,"noPed":0},{"year":2020,"level":"Primary","total":2796,"noPed":57},{"year":2020,"level":"L.Secondary","total":15594,"noPed":174},{"year":2020,"level":"U.Secondary","total":43435,"noPed":454},{"year":2020,"level":"Graduate","total":30568,"noPed":504},{"year":2020,"level":"PostGrad","total":2286,"noPed":56},{"year":2020,"level":"PhD","total":38,"noPed":3}];

const dropoutFlow = [{"year":2018,"grade":"G1","dropout":3.5},{"year":2018,"grade":"G2","dropout":3.5},{"year":2018,"grade":"G3","dropout":4.2},{"year":2018,"grade":"G4","dropout":4.4},{"year":2018,"grade":"G5","dropout":5.0},{"year":2018,"grade":"G6","dropout":6.2},{"year":2018,"grade":"G7","dropout":16.8},{"year":2018,"grade":"G8","dropout":13.9},{"year":2018,"grade":"G9","dropout":16.7},{"year":2018,"grade":"G10","dropout":14.1},{"year":2018,"grade":"G11","dropout":7.2},{"year":2018,"grade":"G12","dropout":30.9},{"year":2019,"grade":"G1","dropout":3.4},{"year":2019,"grade":"G2","dropout":2.8},{"year":2019,"grade":"G3","dropout":3.2},{"year":2019,"grade":"G4","dropout":3.8},{"year":2019,"grade":"G5","dropout":3.9},{"year":2019,"grade":"G6","dropout":19.9},{"year":2019,"grade":"G7","dropout":14.1},{"year":2019,"grade":"G8","dropout":13.8},{"year":2019,"grade":"G9","dropout":26.2},{"year":2019,"grade":"G10","dropout":13.0},{"year":2019,"grade":"G11","dropout":7.3},{"year":2019,"grade":"G12","dropout":26.4},{"year":2020,"grade":"G1","dropout":4.3},{"year":2020,"grade":"G2","dropout":4.8},{"year":2020,"grade":"G3","dropout":4.8},{"year":2020,"grade":"G4","dropout":5.7},{"year":2020,"grade":"G5","dropout":6.4},{"year":2020,"grade":"G6","dropout":23.3},{"year":2020,"grade":"G7","dropout":11.8},{"year":2020,"grade":"G8","dropout":12.6},{"year":2020,"grade":"G9","dropout":28.7},{"year":2020,"grade":"G10","dropout":13.1},{"year":2020,"grade":"G11","dropout":8.0},{"year":2020,"grade":"G12","dropout":38.1}];

const urbanRural2020 = [{"name":"Urban","enrollment":631100,"enrollF":313657,"schools":1464,"teachStaff":22625,"repeaters":30248},{"name":"Rural","enrollment":2645976,"enrollF":1338875,"schools":12217,"teachStaff":72093,"repeaters":145470}];

// ── PALETTE ───────────────────────────────────────────────────────────────────
const C = {
  navy:   "#1B3A5C",
  blue:   "#2E6FAE",
  sky:    "#5BA3D0",
  teal:   "#2BB5A0",
  amber:  "#E8A838",
  coral:  "#D95F4B",
  sage:   "#4E8A6B",
  slate:  "#6B7F94",
  light:  "#F4F7FB",
};
const YEAR_COLORS = { 2018: C.sky, 2019: C.teal, 2020: C.amber };
const GRADES = ["G1","G2","G3","G4","G5","G6","G7","G8","G9","G10","G11","G12"];

const fmt  = (n) => n >= 1_000_000 ? (n/1_000_000).toFixed(1)+"M" : n >= 1000 ? (n/1000).toFixed(1)+"k" : n;
const pct  = (a, b) => b > 0 ? ((a/b)*100).toFixed(1)+"%" : "—";

// ── TOOLTIP ───────────────────────────────────────────────────────────────────
const Tip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background:"#fff", border:"1px solid #dde3ed", borderRadius:8, padding:"10px 14px", fontSize:12, boxShadow:"0 4px 12px rgba(0,0,0,.08)" }}>
      <p style={{ fontWeight:600, marginBottom:6, color:C.navy }}>{label}</p>
      {payload.map((p,i) => (
        <p key={i} style={{ color:p.color, margin:"2px 0" }}>{p.name}: <strong>{typeof p.value==="number" ? p.value.toLocaleString() : p.value}</strong></p>
      ))}
    </div>
  );
};

// ── STAT CARD ─────────────────────────────────────────────────────────────────
const StatCard = ({ label, value, sub, accent = C.blue }) => (
  <div style={{ background:"#fff", borderRadius:10, padding:"16px 18px", borderLeft:`4px solid ${accent}`, boxShadow:"0 1px 6px rgba(0,0,0,.06)" }}>
    <p style={{ fontSize:10, fontWeight:600, letterSpacing:".09em", textTransform:"uppercase", color:C.slate, marginBottom:8 }}>{label}</p>
    <p style={{ fontSize:26, fontWeight:600, color:C.navy, lineHeight:1 }}>{value}</p>
    {sub && <p style={{ fontSize:11, color:C.slate, marginTop:5 }}>{sub}</p>}
  </div>
);

// ── CHART CARD ────────────────────────────────────────────────────────────────
const Card = ({ title, sub, children, style }) => (
  <div style={{ background:"#fff", borderRadius:10, padding:"18px 20px", boxShadow:"0 1px 6px rgba(0,0,0,.06)", ...style }}>
    {title && <p style={{ fontSize:13, fontWeight:600, color:C.navy, marginBottom:2 }}>{title}</p>}
    {sub   && <p style={{ fontSize:11, color:C.slate, marginBottom:14 }}>{sub}</p>}
    {children}
  </div>
);

// ── SECTION HEADER ────────────────────────────────────────────────────────────
const Sec = ({ title, sub }) => (
  <div style={{ margin:"32px 0 14px" }}>
    <h2 style={{ fontSize:16, fontWeight:700, color:C.navy, marginBottom:3 }}>{title}</h2>
    {sub && <p style={{ fontSize:12, color:C.slate }}>{sub}</p>}
  </div>
);

// ── MAIN ──────────────────────────────────────────────────────────────────────
export default function PublicDashboard() {
  const [year, setYear]     = useState(2020);
  const [sortCol, setSort]  = useState("enrollment");
  const [asc, setAsc]       = useState(false);

  const yearData = useMemo(() => overviewRaw.filter(r => r.year === year), [year]);

  // KPIs
  const totSchools   = useMemo(() => yearData.reduce((a,r) => a+r.schools,   0), [yearData]);
  const totEnroll    = useMemo(() => yearData.reduce((a,r) => a+r.enrollment, 0), [yearData]);
  const totEnrollF   = useMemo(() => yearData.reduce((a,r) => a+r.enrollF,   0), [yearData]);
  const totTeach     = useMemo(() => yearData.reduce((a,r) => a+r.teachStaff,0), [yearData]);
  const totRepeaters = useMemo(() => yearData.reduce((a,r) => a+r.repeaters, 0), [yearData]);

  // Top 10 by enrollment
  const top10 = useMemo(() =>
    [...yearData].sort((a,b) => b.enrollment - a.enrollment).slice(0,10)
      .map(r => ({ name: r.province.replace("Banteay Meanchey","B.Meanchey").replace("Kampong Cham","K.Cham").replace("Kampong Chhnang","K.Chhnang").replace("Kampong Speu","K.Speu").replace("Kampong Thom","K.Thom").replace("Preah Vihear","Pr.Vihear"),
        enrollment: r.enrollment, enrollF: r.enrollF }))
  , [yearData]);

  // Dropout pivot for multi-line chart
  const dropoutPivot = useMemo(() =>
    GRADES.map(g => {
      const row = { grade: g };
      [2018,2019,2020].forEach(y => {
        const found = dropoutFlow.find(d => d.year===y && d.grade===g);
        row[`y${y}`] = found ? found.dropout : null;
      });
      return row;
    })
  , []);

  // Sorted province table
  const tableData = useMemo(() => {
    return [...yearData].sort((a,b) => {
      const va = a[sortCol] ?? 0, vb = b[sortCol] ?? 0;
      return asc ? va - vb : vb - va;
    });
  }, [yearData, sortCol, asc]);

  const handleSort = (col) => {
    if (sortCol === col) setAsc(!asc);
    else { setSort(col); setAsc(false); }
  };
  const thStyle = (col) => ({
    cursor: "pointer",
    color: sortCol===col ? C.amber : C.slate,
    fontWeight: sortCol===col ? 700 : 500,
    padding:"10px 12px", fontSize:10, textTransform:"uppercase", letterSpacing:".07em",
    whiteSpace:"nowrap", userSelect:"none", textAlign:"left",
  });

  return (
    <div style={{ fontFamily:"Georgia, 'Times New Roman', serif", background:C.light, minHeight:"100vh", padding:"24px 28px", maxWidth:1120, margin:"0 auto" }}>

      {/* ── HEADER ── */}
      <div style={{ display:"flex", justifyContent:"space-between", alignItems:"flex-start", flexWrap:"wrap", gap:16, marginBottom:28 }}>
        <div>
          <p style={{ fontSize:10, fontWeight:700, letterSpacing:".12em", textTransform:"uppercase", color:C.teal, marginBottom:6 }}>
            Cambodia · Ministry of Education, Youth &amp; Sport
          </p>
          <h1 style={{ fontSize:28, fontWeight:700, color:C.navy, marginBottom:4, fontFamily:"Georgia, serif" }}>Public Schools Dashboard</h1>
          <p style={{ fontSize:12, color:C.slate }}>Academic years 2018–19, 2019–20, 2020–21 · 25 provinces</p>
        </div>
        <div style={{ display:"flex", gap:6, alignItems:"center" }}>
          {[2018,2019,2020].map(y => (
            <button key={y} onClick={() => setYear(y)}
              style={{ padding:"7px 16px", borderRadius:7, fontSize:12, cursor:"pointer", fontFamily:"inherit",
                border:`1.5px solid ${year===y ? C.navy : "#cdd5e0"}`,
                background: year===y ? C.navy : "#fff",
                color: year===y ? "#fff" : C.slate,
                fontWeight: year===y ? 700 : 400 }}>
              {y}–{y-1999}
            </button>
          ))}
        </div>
      </div>

      {/* ── KPI ROW ── */}
      <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(150px,1fr))", gap:12, marginBottom:28 }}>
        <StatCard label="Total Schools"     value={totSchools.toLocaleString()}  sub="Public schools nationwide"     accent={C.navy} />
        <StatCard label="Total Enrollment"  value={fmt(totEnroll)}               sub={`${pct(totEnrollF,totEnroll)} female`} accent={C.teal} />
        <StatCard label="Teaching Staff"    value={totTeach.toLocaleString()}    sub="All teaching staff"             accent={C.blue} />
        <StatCard label="Repeaters"         value={totRepeaters.toLocaleString()} sub={pct(totRepeaters,totEnroll)+" of enrollment"} accent={C.coral} />
        <StatCard label="Students / School" value={Math.round(totEnroll/Math.max(totSchools,1))} sub="National average"    accent={C.sage} />
        <StatCard label="Female Teachers"   value={pct(yearData.reduce((a,r)=>a+r.teachF,0), totTeach)} sub="Share of teaching staff" accent={C.amber} />
      </div>

      {/* ── SECTION 1: ENROLLMENT ── */}
      <Sec title="🏫 Enrollment & Schools" sub="Provincial distribution and gender breakdown" />

      <div style={{ display:"grid", gridTemplateColumns:"2fr 1fr", gap:14, marginBottom:14 }}>
        <Card title="Top 10 Provinces by Enrollment" sub="Total vs female students">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={top10} layout="vertical" margin={{ left:72, right:20, top:4, bottom:4 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#edf0f5" horizontal={false} />
              <XAxis type="number" tickFormatter={fmt} tick={{ fontSize:10, fill:C.slate }} />
              <YAxis type="category" dataKey="name" tick={{ fontSize:10, fill:C.slate }} width={70} />
              <Tooltip content={<Tip />} />
              <Legend wrapperStyle={{ fontSize:11 }} />
              <Bar dataKey="enrollment" name="Total"  fill={C.blue}  radius={[0,3,3,0]} />
              <Bar dataKey="enrollF"   name="Female" fill={C.teal}  radius={[0,3,3,0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Gender Split" sub="Female share of enrollment">
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={[{ name:"Female", value:totEnrollF },{ name:"Male", value:totEnroll-totEnrollF }]}
                cx="50%" cy="50%" outerRadius={78} innerRadius={46} dataKey="value"
                label={({ name, percent }) => `${name} ${(percent*100).toFixed(1)}%`} labelLine={false}>
                <Cell fill={C.teal} />
                <Cell fill={C.blue} />
              </Pie>
              <Tooltip content={<Tip />} />
            </PieChart>
          </ResponsiveContainer>
          <p style={{ textAlign:"center", fontSize:11, color:C.slate, marginTop:4 }}>
            {totEnrollF.toLocaleString()} female · {(totEnroll-totEnrollF).toLocaleString()} male
          </p>
        </Card>
      </div>

      {/* National trend */}
      <Card title="National Trends — Three Academic Years" sub="Schools, enrollment, and teaching staff" style={{ marginBottom:14 }}>
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={nationalTotals} margin={{ left:10, right:20, top:8, bottom:4 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#edf0f5" />
            <XAxis dataKey="year" tick={{ fontSize:11, fill:C.slate }} />
            <YAxis yAxisId="l" tickFormatter={fmt} tick={{ fontSize:10, fill:C.slate }} />
            <YAxis yAxisId="r" orientation="right" tickFormatter={fmt} tick={{ fontSize:10, fill:C.slate }} />
            <Tooltip content={<Tip />} />
            <Legend wrapperStyle={{ fontSize:11 }} />
            <Line yAxisId="l" type="monotone" dataKey="enrollment" name="Enrollment"      stroke={C.blue}  strokeWidth={2} dot={{ r:4 }} />
            <Line yAxisId="l" type="monotone" dataKey="teachStaff" name="Teaching Staff"  stroke={C.amber} strokeWidth={2} dot={{ r:4 }} />
            <Line yAxisId="r" type="monotone" dataKey="schools"    name="Schools"         stroke={C.navy}  strokeWidth={2} dot={{ r:4 }} strokeDasharray="5 3" />
          </LineChart>
        </ResponsiveContainer>
      </Card>

      {/* Urban vs Rural */}
      <Sec title="🏙️ Urban vs Rural Split (2020–21)" sub="Schools, enrollment and teaching staff — Whole Kingdom" />

      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14, marginBottom:14 }}>
        <Card title="Enrollment & Staff by Area">
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={urbanRural2020} margin={{ left:10, right:10, top:4, bottom:4 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#edf0f5" />
              <XAxis dataKey="name" tick={{ fontSize:12, fill:C.slate }} />
              <YAxis tickFormatter={fmt} tick={{ fontSize:10, fill:C.slate }} />
              <Tooltip content={<Tip />} />
              <Legend wrapperStyle={{ fontSize:11 }} />
              <Bar dataKey="enrollment"  name="Enrollment"      fill={C.blue}  radius={[3,3,0,0]} />
              <Bar dataKey="teachStaff" name="Teaching Staff"  fill={C.amber} radius={[3,3,0,0]} />
              <Bar dataKey="schools"    name="Schools"         fill={C.teal}  radius={[3,3,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Urban vs Rural Enrollment Share" sub="% of national total">
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={urbanRural2020} cx="50%" cy="50%" outerRadius={80} innerRadius={46}
                dataKey="enrollment" nameKey="name"
                label={({ name, percent }) => `${name} ${(percent*100).toFixed(0)}%`} labelLine={false}>
                <Cell fill={C.navy} />
                <Cell fill={C.sage} />
              </Pie>
              <Tooltip content={<Tip />} />
            </PieChart>
          </ResponsiveContainer>
          <p style={{ textAlign:"center", fontSize:11, color:C.slate }}>
            Urban {((631100/3277076)*100).toFixed(1)}% · Rural {((2645976/3277076)*100).toFixed(1)}%
          </p>
        </Card>
      </div>

      {/* ── SECTION 2: STAFF ── */}
      <Sec title="👩‍🏫 Teaching Staff" sub="Education qualification breakdown — national totals (2018 vs 2020)" />

      <Card title="Staff by Qualification Level" sub="Comparing 2018 and 2020 · no-pedagogical-training shown in coral" style={{ marginBottom:14 }}>
        <ResponsiveContainer width="100%" height={240}>
          <BarChart
            data={["Primary","L.Secondary","U.Secondary","Graduate","PostGrad","PhD"].map(lv => {
              const r18 = staffQual.find(s => s.year===2018 && s.level===lv) || {};
              const r20 = staffQual.find(s => s.year===2020 && s.level===lv) || {};
              return { level:lv, total18:r18.total||0, total20:r20.total||0, noPed18:r18.noPed||0, noPed20:r20.noPed||0 };
            })}
            margin={{ left:10, right:10, top:4, bottom:4 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#edf0f5" />
            <XAxis dataKey="level" tick={{ fontSize:10, fill:C.slate }} />
            <YAxis tickFormatter={fmt} tick={{ fontSize:10, fill:C.slate }} />
            <Tooltip content={<Tip />} />
            <Legend wrapperStyle={{ fontSize:11 }} />
            <Bar dataKey="total18" name="Total 2018"        fill={C.sky}   radius={[3,3,0,0]} />
            <Bar dataKey="total20" name="Total 2020"        fill={C.blue}  radius={[3,3,0,0]} />
            <Bar dataKey="noPed20" name="No Ped. Trng 2020" fill={C.coral} radius={[3,3,0,0]} />
          </BarChart>
        </ResponsiveContainer>
      </Card>

      {/* ── SECTION 3: DROPOUT ── */}
      <Sec title="📉 Student Dropout Rates" sub="% of students leaving school by grade — Whole Kingdom (all three years)" />

      <Card title="Dropout Rate by Grade" sub="Note: Sharp spike at G6→G7 reflects the primary-to-secondary transition" style={{ marginBottom:14 }}>
        <ResponsiveContainer width="100%" height={260}>
          <AreaChart data={dropoutPivot} margin={{ left:10, right:20, top:8, bottom:4 }}>
            <defs>
              {[2018,2019,2020].map(y => (
                <linearGradient key={y} id={`grad${y}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor={YEAR_COLORS[y]} stopOpacity={0.25} />
                  <stop offset="95%" stopColor={YEAR_COLORS[y]} stopOpacity={0.03} />
                </linearGradient>
              ))}
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#edf0f5" />
            <XAxis dataKey="grade" tick={{ fontSize:11, fill:C.slate }} />
            <YAxis tickFormatter={v => v+"%"} tick={{ fontSize:10, fill:C.slate }} />
            <Tooltip content={<Tip />} formatter={(v,n) => [v+"%", n]} />
            <Legend wrapperStyle={{ fontSize:11 }} />
            {[2018,2019,2020].map(y => (
              <Area key={y} type="monotone" dataKey={`y${y}`} name={`${y}–${y-1999}`}
                stroke={YEAR_COLORS[y]} strokeWidth={2}
                fill={`url(#grad${y})`} dot={{ r:3, fill:YEAR_COLORS[y] }} connectNulls />
            ))}
          </AreaChart>
        </ResponsiveContainer>
      </Card>

      {/* Repeaters trend */}
      <Sec title="🔁 Grade Repeaters" sub="Students repeating a grade — national totals and rate relative to enrollment" />

      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:14, marginBottom:14 }}>
        <Card title="Total Repeaters by Year">
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={nationalTotals} margin={{ left:10, right:10, top:4, bottom:4 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#edf0f5" />
              <XAxis dataKey="year" tick={{ fontSize:11, fill:C.slate }} />
              <YAxis tickFormatter={fmt} tick={{ fontSize:10, fill:C.slate }} />
              <Tooltip content={<Tip />} />
              <Bar dataKey="repeaters" name="Repeaters" fill={C.coral} radius={[3,3,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Repeater Rate (% of Enrollment)">
          <ResponsiveContainer width="100%" height={220}>
            <BarChart
              data={nationalTotals.map(r => ({ year:r.year, rate: parseFloat(((r.repeaters/r.enrollment)*100).toFixed(2)) }))}
              margin={{ left:0, right:10, top:4, bottom:4 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#edf0f5" />
              <XAxis dataKey="year" tick={{ fontSize:11, fill:C.slate }} />
              <YAxis tickFormatter={v => v+"%"} tick={{ fontSize:10, fill:C.slate }} />
              <Tooltip content={<Tip />} formatter={v => [v+"%","Repeater rate"]} />
              <Bar dataKey="rate" name="Repeater rate %" fill={C.amber} radius={[3,3,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* ── SECTION 4: PROVINCE TABLE ── */}
      <Sec title="📊 Province Rankings" sub={`Click column headers to sort · ${year}–${year-1999} data`} />

      <div style={{ border:"1px solid #dde3ed", borderRadius:10, overflow:"hidden", background:"#fff", boxShadow:"0 1px 6px rgba(0,0,0,.05)", marginBottom:32 }}>
        <div style={{ overflowX:"auto" }}>
          <table style={{ width:"100%", borderCollapse:"collapse", fontSize:12 }}>
            <thead>
              <tr style={{ background:C.navy, borderBottom:`2px solid ${C.navy}` }}>
                {[
                  ["Province",   "province"],
                  ["Schools",    "schools"],
                  ["Enrollment", "enrollment"],
                  ["% Female",   null],
                  ["Repeaters",  "repeaters"],
                  ["Rep. Rate",  null],
                  ["Teachers",   "teachStaff"],
                  ["% Female T", null],
                  ["Stu/School", null],
                ].map(([label, col]) => (
                  <th key={label} onClick={col ? () => handleSort(col) : undefined}
                    style={{ ...thStyle(col), color: sortCol===col ? C.amber : "#c8d8ea" }}>
                    {label}{col ? (sortCol===col ? (asc?" ↑":" ↓") : " ↕") : ""}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {tableData.map((r, i) => {
                const repRate = ((r.repeaters/Math.max(r.enrollment,1))*100).toFixed(1);
                const teachFPct = ((r.teachF/Math.max(r.teachStaff,1))*100).toFixed(0);
                return (
                  <tr key={r.province+r.year}
                    style={{ borderBottom:"1px solid #edf0f5", background: i%2===0 ? "#fff" : C.light }}>
                    <td style={{ padding:"8px 12px", fontWeight:600, color:C.navy, whiteSpace:"nowrap" }}>{r.province}</td>
                    <td style={{ padding:"8px 12px", color:C.navy }}>{r.schools.toLocaleString()}</td>
                    <td style={{ padding:"8px 12px", color:C.navy }}>{r.enrollment.toLocaleString()}</td>
                    <td style={{ padding:"8px 12px" }}>
                      <span style={{ background:"#e8f5f2", color:C.teal, padding:"2px 8px", borderRadius:20, fontSize:10, fontWeight:700 }}>
                        {pct(r.enrollF, r.enrollment)}
                      </span>
                    </td>
                    <td style={{ padding:"8px 12px", color:C.coral, fontWeight:600 }}>{r.repeaters.toLocaleString()}</td>
                    <td style={{ padding:"8px 12px" }}>
                      <span style={{ background: parseFloat(repRate)>6 ? "#fde8e5" : "#fef3e0",
                        color: parseFloat(repRate)>6 ? C.coral : C.amber,
                        padding:"2px 8px", borderRadius:20, fontSize:10, fontWeight:700 }}>
                        {repRate}%
                      </span>
                    </td>
                    <td style={{ padding:"8px 12px", color:C.navy }}>{r.teachStaff.toLocaleString()}</td>
                    <td style={{ padding:"8px 12px", color:C.slate }}>{teachFPct}%</td>
                    <td style={{ padding:"8px 12px", color:C.slate }}>{Math.round(r.enrollment/Math.max(r.schools,1))}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* FOOTER */}
      <p style={{ fontSize:10, color:C.slate, textAlign:"center", marginTop:8 }}>
        Data source: Cambodia Ministry of Education, Youth and Sport · Public Schools Statistics 2018–19, 2019–20, 2020–21
      </p>
    </div>
  );
}
