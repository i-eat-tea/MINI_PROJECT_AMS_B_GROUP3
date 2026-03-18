import { useState, useMemo } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  LineChart, Line, PieChart, Pie, Cell, ResponsiveContainer,
  RadarChart, Radar, PolarGrid, PolarAngleAxis,
} from "recharts";

// ── DATA ─────────────────────────────────────────────────────────────────────
const overviewRaw      = [{"province":"Banteay Meanchey","year":2018,"schools":121,"classes":894,"enrollment":21942,"enrollF":10611,"teachStaff":1053,"teachF":580,"nonTeach":252,"nonTeachF":113,"foreignTeach":49,"buildings":132,"rooms":1382,"classrooms":703},{"province":"Battambang","year":2018,"schools":45,"classes":406,"enrollment":8804,"enrollF":4371,"teachStaff":779,"teachF":488,"nonTeach":165,"nonTeachF":82,"foreignTeach":38,"buildings":57,"rooms":632,"classrooms":361},{"province":"Kampong Cham","year":2018,"schools":25,"classes":158,"enrollment":4010,"enrollF":1969,"teachStaff":214,"teachF":130,"nonTeach":34,"nonTeachF":14,"foreignTeach":7,"buildings":52,"rooms":295,"classrooms":140},{"province":"Kampong Chhnang","year":2018,"schools":25,"classes":190,"enrollment":4505,"enrollF":2055,"teachStaff":356,"teachF":242,"nonTeach":87,"nonTeachF":46,"foreignTeach":13,"buildings":51,"rooms":326,"classrooms":183},{"province":"Kampong Speu","year":2018,"schools":50,"classes":328,"enrollment":8134,"enrollF":4179,"teachStaff":444,"teachF":279,"nonTeach":109,"nonTeachF":41,"foreignTeach":49,"buildings":67,"rooms":517,"classrooms":296},{"province":"Kampong Thom","year":2018,"schools":14,"classes":100,"enrollment":2143,"enrollF":1055,"teachStaff":155,"teachF":88,"nonTeach":28,"nonTeachF":12,"foreignTeach":4,"buildings":24,"rooms":183,"classrooms":92},{"province":"Kampot","year":2018,"schools":20,"classes":110,"enrollment":2516,"enrollF":1235,"teachStaff":188,"teachF":102,"nonTeach":32,"nonTeachF":13,"foreignTeach":6,"buildings":25,"rooms":200,"classrooms":97},{"province":"Kandal","year":2018,"schools":75,"classes":461,"enrollment":9989,"enrollF":5066,"teachStaff":663,"teachF":415,"nonTeach":131,"nonTeachF":64,"foreignTeach":13,"buildings":98,"rooms":790,"classrooms":415},{"province":"Kep","year":2018,"schools":3,"classes":13,"enrollment":213,"enrollF":104,"teachStaff":16,"teachF":9,"nonTeach":6,"nonTeachF":3,"foreignTeach":0,"buildings":3,"rooms":19,"classrooms":11},{"province":"Koh Kong","year":2018,"schools":7,"classes":43,"enrollment":744,"enrollF":358,"teachStaff":60,"teachF":33,"nonTeach":14,"nonTeachF":6,"foreignTeach":2,"buildings":8,"rooms":59,"classrooms":32},{"province":"Kratie","year":2018,"schools":5,"classes":34,"enrollment":683,"enrollF":321,"teachStaff":52,"teachF":30,"nonTeach":9,"nonTeachF":3,"foreignTeach":2,"buildings":7,"rooms":52,"classrooms":26},{"province":"Mondulkiri","year":2018,"schools":2,"classes":10,"enrollment":153,"enrollF":74,"teachStaff":14,"teachF":7,"nonTeach":4,"nonTeachF":1,"foreignTeach":0,"buildings":2,"rooms":14,"classrooms":8},{"province":"Oddar Meanchey","year":2018,"schools":6,"classes":28,"enrollment":489,"enrollF":219,"teachStaff":38,"teachF":20,"nonTeach":9,"nonTeachF":3,"foreignTeach":0,"buildings":6,"rooms":43,"classrooms":22},{"province":"Pailin","year":2018,"schools":4,"classes":20,"enrollment":375,"enrollF":165,"teachStaff":28,"teachF":14,"nonTeach":7,"nonTeachF":2,"foreignTeach":0,"buildings":4,"rooms":29,"classrooms":14},{"province":"Phnom Penh","year":2018,"schools":393,"classes":3044,"enrollment":75128,"enrollF":36428,"teachStaff":4950,"teachF":3145,"nonTeach":1426,"nonTeachF":711,"foreignTeach":1191,"buildings":574,"rooms":6942,"classrooms":3211},{"province":"Preah Sihanouk","year":2018,"schools":48,"classes":319,"enrollment":6820,"enrollF":3159,"teachStaff":659,"teachF":380,"nonTeach":150,"nonTeachF":67,"foreignTeach":143,"buildings":63,"rooms":637,"classrooms":301},{"province":"Preah Vihear","year":2018,"schools":3,"classes":14,"enrollment":248,"enrollF":113,"teachStaff":18,"teachF":9,"nonTeach":4,"nonTeachF":1,"foreignTeach":0,"buildings":3,"rooms":21,"classrooms":11},{"province":"Prey Veng","year":2018,"schools":27,"classes":156,"enrollment":3463,"enrollF":1677,"teachStaff":237,"teachF":139,"nonTeach":38,"nonTeachF":16,"foreignTeach":5,"buildings":33,"rooms":249,"classrooms":127},{"province":"Pursat","year":2018,"schools":12,"classes":59,"enrollment":1272,"enrollF":581,"teachStaff":88,"teachF":47,"nonTeach":19,"nonTeachF":7,"foreignTeach":2,"buildings":13,"rooms":92,"classrooms":46},{"province":"Ratanakiri","year":2018,"schools":2,"classes":8,"enrollment":108,"enrollF":48,"teachStaff":8,"teachF":4,"nonTeach":2,"nonTeachF":1,"foreignTeach":0,"buildings":2,"rooms":8,"classrooms":5},{"province":"Siem Reap","year":2018,"schools":89,"classes":580,"enrollment":13440,"enrollF":6609,"teachStaff":1061,"teachF":617,"nonTeach":231,"nonTeachF":101,"foreignTeach":176,"buildings":122,"rooms":1228,"classrooms":595},{"province":"Stung Treng","year":2018,"schools":4,"classes":16,"enrollment":264,"enrollF":124,"teachStaff":19,"teachF":9,"nonTeach":4,"nonTeachF":1,"foreignTeach":0,"buildings":4,"rooms":21,"classrooms":12},{"province":"Svay Rieng","year":2018,"schools":14,"classes":87,"enrollment":1902,"enrollF":885,"teachStaff":131,"teachF":70,"nonTeach":22,"nonTeachF":8,"foreignTeach":3,"buildings":16,"rooms":127,"classrooms":65},{"province":"Takeo","year":2018,"schools":28,"classes":147,"enrollment":3252,"enrollF":1460,"teachStaff":231,"teachF":116,"nonTeach":37,"nonTeachF":14,"foreignTeach":6,"buildings":30,"rooms":218,"classrooms":103},{"province":"Tbaung Khmum","year":2018,"schools":13,"classes":68,"enrollment":1393,"enrollF":651,"teachStaff":93,"teachF":51,"nonTeach":18,"nonTeachF":7,"foreignTeach":2,"buildings":13,"rooms":98,"classrooms":48},{"province":"Banteay Meanchey","year":2019,"schools":130,"classes":952,"enrollment":23800,"enrollF":11500,"teachStaff":1120,"teachF":615,"nonTeach":270,"nonTeachF":121,"foreignTeach":52,"buildings":140,"rooms":1480,"classrooms":750},{"province":"Battambang","year":2019,"schools":48,"classes":430,"enrollment":9300,"enrollF":4620,"teachStaff":820,"teachF":510,"nonTeach":174,"nonTeachF":87,"foreignTeach":41,"buildings":61,"rooms":668,"classrooms":381},{"province":"Kampong Cham","year":2019,"schools":27,"classes":168,"enrollment":4250,"enrollF":2088,"teachStaff":226,"teachF":138,"nonTeach":36,"nonTeachF":15,"foreignTeach":8,"buildings":55,"rooms":312,"classrooms":148},{"province":"Kampong Chhnang","year":2019,"schools":26,"classes":198,"enrollment":4680,"enrollF":2135,"teachStaff":368,"teachF":250,"nonTeach":91,"nonTeachF":48,"foreignTeach":14,"buildings":53,"rooms":340,"classrooms":190},{"province":"Kampong Speu","year":2019,"schools":53,"classes":348,"enrollment":8640,"enrollF":4430,"teachStaff":467,"teachF":293,"nonTeach":115,"nonTeachF":43,"foreignTeach":51,"buildings":71,"rooms":545,"classrooms":311},{"province":"Kampong Thom","year":2019,"schools":15,"classes":108,"enrollment":2280,"enrollF":1120,"teachStaff":163,"teachF":93,"nonTeach":30,"nonTeachF":13,"foreignTeach":5,"buildings":26,"rooms":193,"classrooms":97},{"province":"Kampot","year":2019,"schools":21,"classes":116,"enrollment":2660,"enrollF":1305,"teachStaff":197,"teachF":107,"nonTeach":34,"nonTeachF":14,"foreignTeach":7,"buildings":27,"rooms":211,"classrooms":102},{"province":"Kandal","year":2019,"schools":79,"classes":487,"enrollment":10540,"enrollF":5343,"teachStaff":698,"teachF":437,"nonTeach":138,"nonTeachF":68,"foreignTeach":14,"buildings":104,"rooms":832,"classrooms":438},{"province":"Kep","year":2019,"schools":3,"classes":14,"enrollment":225,"enrollF":110,"teachStaff":17,"teachF":10,"nonTeach":6,"nonTeachF":3,"foreignTeach":0,"buildings":3,"rooms":20,"classrooms":12},{"province":"Koh Kong","year":2019,"schools":8,"classes":46,"enrollment":789,"enrollF":380,"teachStaff":64,"teachF":35,"nonTeach":15,"nonTeachF":7,"foreignTeach":2,"buildings":9,"rooms":63,"classrooms":34},{"province":"Kratie","year":2019,"schools":6,"classes":37,"enrollment":724,"enrollF":340,"teachStaff":56,"teachF":32,"nonTeach":10,"nonTeachF":4,"foreignTeach":2,"buildings":8,"rooms":56,"classrooms":28},{"province":"Mondulkiri","year":2019,"schools":2,"classes":11,"enrollment":162,"enrollF":79,"teachStaff":15,"teachF":8,"nonTeach":4,"nonTeachF":2,"foreignTeach":0,"buildings":2,"rooms":15,"classrooms":8},{"province":"Oddar Meanchey","year":2019,"schools":7,"classes":30,"enrollment":520,"enrollF":234,"teachStaff":40,"teachF":21,"nonTeach":10,"nonTeachF":3,"foreignTeach":0,"buildings":7,"rooms":46,"classrooms":24},{"province":"Pailin","year":2019,"schools":4,"classes":21,"enrollment":390,"enrollF":172,"teachStaff":29,"teachF":15,"nonTeach":7,"nonTeachF":2,"foreignTeach":0,"buildings":4,"rooms":30,"classrooms":15},{"province":"Phnom Penh","year":2019,"schools":418,"classes":3218,"enrollment":80100,"enrollF":38780,"teachStaff":5300,"teachF":3360,"nonTeach":1520,"nonTeachF":758,"foreignTeach":1270,"buildings":610,"rooms":7380,"classrooms":3420},{"province":"Preah Sihanouk","year":2019,"schools":51,"classes":338,"enrollment":7240,"enrollF":3350,"teachStaff":698,"teachF":402,"nonTeach":159,"nonTeachF":71,"foreignTeach":152,"buildings":67,"rooms":674,"classrooms":319},{"province":"Preah Vihear","year":2019,"schools":3,"classes":15,"enrollment":263,"enrollF":120,"teachStaff":19,"teachF":10,"nonTeach":4,"nonTeachF":1,"foreignTeach":0,"buildings":3,"rooms":22,"classrooms":12},{"province":"Prey Veng","year":2019,"schools":29,"classes":166,"enrollment":3670,"enrollF":1778,"teachStaff":251,"teachF":147,"nonTeach":40,"nonTeachF":17,"foreignTeach":5,"buildings":35,"rooms":264,"classrooms":134},{"province":"Pursat","year":2019,"schools":13,"classes":63,"enrollment":1350,"enrollF":617,"teachStaff":93,"teachF":50,"nonTeach":20,"nonTeachF":8,"foreignTeach":2,"buildings":14,"rooms":98,"classrooms":49},{"province":"Ratanakiri","year":2019,"schools":2,"classes":9,"enrollment":115,"enrollF":51,"teachStaff":9,"teachF":4,"nonTeach":2,"nonTeachF":1,"foreignTeach":0,"buildings":2,"rooms":9,"classrooms":5},{"province":"Siem Reap","year":2019,"schools":94,"classes":614,"enrollment":14280,"enrollF":7020,"teachStaff":1124,"teachF":654,"nonTeach":245,"nonTeachF":107,"foreignTeach":188,"buildings":130,"rooms":1302,"classrooms":631},{"province":"Stung Treng","year":2019,"schools":4,"classes":17,"enrollment":280,"enrollF":131,"teachStaff":20,"teachF":10,"nonTeach":5,"nonTeachF":2,"foreignTeach":0,"buildings":4,"rooms":23,"classrooms":13},{"province":"Svay Rieng","year":2019,"schools":15,"classes":92,"enrollment":2015,"enrollF":938,"teachStaff":139,"teachF":74,"nonTeach":23,"nonTeachF":9,"foreignTeach":3,"buildings":17,"rooms":135,"classrooms":69},{"province":"Takeo","year":2019,"schools":30,"classes":155,"enrollment":3450,"enrollF":1548,"teachStaff":244,"teachF":123,"nonTeach":39,"nonTeachF":15,"foreignTeach":7,"buildings":32,"rooms":231,"classrooms":109},{"province":"Tbaung Khmum","year":2019,"schools":14,"classes":73,"enrollment":1480,"enrollF":691,"teachStaff":98,"teachF":54,"nonTeach":19,"nonTeachF":8,"foreignTeach":2,"buildings":14,"rooms":104,"classrooms":51},{"province":"Banteay Meanchey","year":2020,"schools":134,"classes":980,"enrollment":24500,"enrollF":11840,"teachStaff":1156,"teachF":635,"nonTeach":280,"nonTeachF":125,"foreignTeach":48,"buildings":145,"rooms":1520,"classrooms":773},{"province":"Battambang","year":2020,"schools":49,"classes":440,"enrollment":9520,"enrollF":4730,"teachStaff":839,"teachF":521,"nonTeach":178,"nonTeachF":89,"foreignTeach":38,"buildings":63,"rooms":682,"classrooms":390},{"province":"Kampong Cham","year":2020,"schools":27,"classes":170,"enrollment":4320,"enrollF":2124,"teachStaff":231,"teachF":141,"nonTeach":37,"nonTeachF":16,"foreignTeach":7,"buildings":56,"rooms":318,"classrooms":151},{"province":"Kampong Chhnang","year":2020,"schools":26,"classes":201,"enrollment":4760,"enrollF":2175,"teachStaff":374,"teachF":255,"nonTeach":93,"nonTeachF":49,"foreignTeach":13,"buildings":54,"rooms":347,"classrooms":193},{"province":"Kampong Speu","year":2020,"schools":54,"classes":358,"enrollment":8850,"enrollF":4540,"teachStaff":479,"teachF":300,"nonTeach":118,"nonTeachF":45,"foreignTeach":46,"buildings":73,"rooms":558,"classrooms":318},{"province":"Kampong Thom","year":2020,"schools":15,"classes":111,"enrollment":2330,"enrollF":1145,"teachStaff":167,"teachF":95,"nonTeach":31,"nonTeachF":13,"foreignTeach":4,"buildings":27,"rooms":198,"classrooms":99},{"province":"Kampot","year":2020,"schools":22,"classes":119,"enrollment":2720,"enrollF":1335,"teachStaff":201,"teachF":109,"nonTeach":35,"nonTeachF":14,"foreignTeach":6,"buildings":28,"rooms":217,"classrooms":105},{"province":"Kandal","year":2020,"schools":81,"classes":499,"enrollment":10790,"enrollF":5469,"teachStaff":714,"teachF":447,"nonTeach":142,"nonTeachF":70,"foreignTeach":12,"buildings":107,"rooms":851,"classrooms":448},{"province":"Kep","year":2020,"schools":3,"classes":14,"enrollment":230,"enrollF":113,"teachStaff":17,"teachF":10,"nonTeach":6,"nonTeachF":3,"foreignTeach":0,"buildings":3,"rooms":21,"classrooms":12},{"province":"Koh Kong","year":2020,"schools":8,"classes":47,"enrollment":803,"enrollF":387,"teachStaff":65,"teachF":36,"nonTeach":15,"nonTeachF":7,"foreignTeach":2,"buildings":9,"rooms":64,"classrooms":35},{"province":"Kratie","year":2020,"schools":6,"classes":38,"enrollment":740,"enrollF":348,"teachStaff":58,"teachF":33,"nonTeach":10,"nonTeachF":4,"foreignTeach":2,"buildings":8,"rooms":58,"classrooms":29},{"province":"Mondulkiri","year":2020,"schools":2,"classes":11,"enrollment":165,"enrollF":80,"teachStaff":15,"teachF":8,"nonTeach":4,"nonTeachF":2,"foreignTeach":0,"buildings":2,"rooms":15,"classrooms":8},{"province":"Oddar Meanchey","year":2020,"schools":7,"classes":31,"enrollment":533,"enrollF":240,"teachStaff":41,"teachF":22,"nonTeach":10,"nonTeachF":4,"foreignTeach":0,"buildings":7,"rooms":47,"classrooms":25},{"province":"Pailin","year":2020,"schools":4,"classes":22,"enrollment":400,"enrollF":177,"teachStaff":30,"teachF":16,"nonTeach":7,"nonTeachF":2,"foreignTeach":0,"buildings":4,"rooms":31,"classrooms":16},{"province":"Phnom Penh","year":2020,"schools":432,"classes":3330,"enrollment":83200,"enrollF":40260,"teachStaff":5520,"teachF":3490,"nonTeach":1580,"nonTeachF":788,"foreignTeach":1240,"buildings":632,"rooms":7650,"classrooms":3541},{"province":"Preah Sihanouk","year":2020,"schools":52,"classes":274,"enrollment":5697,"enrollF":2797,"teachStaff":468,"teachF":241,"nonTeach":181,"nonTeachF":91,"foreignTeach":22,"buildings":170,"rooms":593,"classrooms":268},{"province":"Preah Vihear","year":2020,"schools":3,"classes":16,"enrollment":270,"enrollF":123,"teachStaff":20,"teachF":11,"nonTeach":4,"nonTeachF":2,"foreignTeach":0,"buildings":3,"rooms":23,"classrooms":12},{"province":"Prey Veng","year":2020,"schools":30,"classes":170,"enrollment":3760,"enrollF":1820,"teachStaff":258,"teachF":151,"nonTeach":41,"nonTeachF":18,"foreignTeach":5,"buildings":36,"rooms":271,"classrooms":138},{"province":"Pursat","year":2020,"schools":13,"classes":65,"enrollment":1380,"enrollF":631,"teachStaff":96,"teachF":51,"nonTeach":21,"nonTeachF":8,"foreignTeach":2,"buildings":14,"rooms":101,"classrooms":50},{"province":"Ratanakiri","year":2020,"schools":2,"classes":9,"enrollment":118,"enrollF":53,"teachStaff":9,"teachF":5,"nonTeach":2,"nonTeachF":1,"foreignTeach":0,"buildings":2,"rooms":10,"classrooms":5},{"province":"Siem Reap","year":2020,"schools":97,"classes":630,"enrollment":14720,"enrollF":7230,"teachStaff":1150,"teachF":668,"nonTeach":251,"nonTeachF":110,"foreignTeach":162,"buildings":134,"rooms":1335,"classrooms":648},{"province":"Stung Treng","year":2020,"schools":4,"classes":17,"enrollment":285,"enrollF":134,"teachStaff":21,"teachF":11,"nonTeach":5,"nonTeachF":2,"foreignTeach":0,"buildings":4,"rooms":23,"classrooms":13},{"province":"Svay Rieng","year":2020,"schools":16,"classes":95,"enrollment":2070,"enrollF":963,"teachStaff":143,"teachF":77,"nonTeach":24,"nonTeachF":10,"foreignTeach":3,"buildings":18,"rooms":139,"classrooms":71},{"province":"Takeo","year":2020,"schools":27,"classes":164,"enrollment":4692,"enrollF":2671,"teachStaff":243,"teachF":155,"nonTeach":34,"nonTeachF":19,"foreignTeach":28,"buildings":43,"rooms":401,"classrooms":164},{"province":"Tbaung Khmum","year":2020,"schools":16,"classes":80,"enrollment":1560,"enrollF":728,"teachStaff":104,"teachF":57,"nonTeach":21,"nonTeachF":9,"foreignTeach":3,"buildings":15,"rooms":112,"classrooms":55}];
const nationalTotals   = [{"year":"2018\u201319","schools":1050,"enrollment":170739,"teachStaff":11513,"repeaters":2832,"foreignTeach":1709},{"year":"2019\u201320","schools":1117,"enrollment":186745,"teachStaff":12285,"repeaters":2100,"foreignTeach":1839},{"year":"2020\u201321","schools":1666,"enrollment":240550,"teachStaff":15302,"repeaters":1980,"foreignTeach":3298}];
const staffQual        = [{"year":2018,"level":"Primary","total":325,"female":241,"noPed":45},{"year":2018,"level":"L.Secondary","total":621,"female":444,"noPed":72},{"year":2018,"level":"U.Secondary","total":3290,"female":2231,"noPed":312},{"year":2018,"level":"Graduate","total":6480,"female":3820,"noPed":620},{"year":2018,"level":"PostGrad","total":741,"female":280,"noPed":56},{"year":2018,"level":"PhD","total":56,"female":14,"noPed":2},{"year":2020,"level":"Primary","total":582,"female":403,"noPed":75},{"year":2020,"level":"L.Secondary","total":892,"female":638,"noPed":97},{"year":2020,"level":"U.Secondary","total":4169,"female":2986,"noPed":485},{"year":2020,"level":"Graduate","total":8568,"female":4762,"noPed":898},{"year":2020,"level":"PostGrad","total":998,"female":359,"noPed":77},{"year":2020,"level":"PhD","total":93,"female":31,"noPed":3}];
const repeatersByGrade = [{"grade":"G1","total":614,"girls":253},{"grade":"G2","total":486,"girls":219},{"grade":"G3","total":371,"girls":156},{"grade":"G4","total":280,"girls":118},{"grade":"G5","total":198,"girls":82},{"grade":"G6","total":152,"girls":64},{"grade":"G7","total":134,"girls":55},{"grade":"G8","total":118,"girls":49},{"grade":"G9","total":98,"girls":41},{"grade":"G10","total":87,"girls":35},{"grade":"G11","total":20,"girls":8},{"grade":"G12","total":79,"girls":37}];
const urbanRural2020   = [{"name":"Urban","enrollment":196707,"schools":1320,"teachStaff":12631},{"name":"Rural","enrollment":43843,"schools":346,"teachStaff":2671}];
const facilities       = {"2018":{"Computer":2890,"Printer":2310,"LCD_Projector":1680,"Photocopy":1890,"Library":1540,"Resource_Center":420,"Drinking_Water":3210,"Toilet":3840},"2020":{"Computer":24041,"Printer":1835,"LCD_Projector":2977,"Photocopy":1707,"Library":3129,"Resource_Center":561,"Drinking_Water":1418,"Health_Room":1126,"Computer_Room":1140}};

const COLORS = {
  blue:   "#4A90D9",
  teal:   "#2BB5A0",
  amber:  "#E8A838",
  coral:  "#E05D5D",
  purple: "#7B6FD8",
  green:  "#52A852",
  gray:   "#8A9BAB",
};
const YEAR_COLORS = { 2018: COLORS.blue, 2019: COLORS.teal, 2020: COLORS.amber };

const fmt = (n) => n >= 1000 ? (n / 1000).toFixed(1) + "k" : n;
const pct = (a, b) => b > 0 ? ((a / b) * 100).toFixed(1) + "%" : "—";

// ─── CUSTOM TOOLTIP ───────────────────────────────────────────────────────
const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-secondary)", borderRadius: 8, padding: "10px 14px", fontSize: 13 }}>
      <p style={{ fontWeight: 500, marginBottom: 6, color: "var(--color-text-primary)" }}>{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.color, margin: "2px 0" }}>{p.name}: <strong>{p.value?.toLocaleString()}</strong></p>
      ))}
    </div>
  );
};

// ─── STAT CARD ────────────────────────────────────────────────────────────
const StatCard = ({ label, value, sub, color = COLORS.blue, delta }) => (
  <div style={{ background: "var(--color-background-secondary)", borderRadius: 12, padding: "16px 18px", borderTop: `3px solid ${color}` }}>
    <p style={{ fontSize: 11, fontWeight: 500, letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--color-text-secondary)", marginBottom: 8 }}>{label}</p>
    <p style={{ fontSize: 28, fontWeight: 500, color: "var(--color-text-primary)", lineHeight: 1 }}>{value}</p>
    {sub && <p style={{ fontSize: 12, color: "var(--color-text-secondary)", marginTop: 5 }}>{sub}</p>}
    {delta != null && (
      <p style={{ fontSize: 12, marginTop: 5, color: delta >= 0 ? COLORS.teal : COLORS.coral, fontWeight: 500 }}>
        {delta >= 0 ? "▲" : "▼"} {Math.abs(delta)}% vs prev year
      </p>
    )}
  </div>
);

// ─── SECTION HEADER ───────────────────────────────────────────────────────
const SectionHeader = ({ title, sub }) => (
  <div style={{ marginBottom: 16, marginTop: 32 }}>
    <h2 style={{ fontSize: 18, fontWeight: 500, color: "var(--color-text-primary)", marginBottom: 4 }}>{title}</h2>
    <p style={{ fontSize: 13, color: "var(--color-text-secondary)" }}>{sub}</p>
  </div>
);

// ─── CHART CARD ──────────────────────────────────────────────────────────
const ChartCard = ({ title, sub, children, style }) => (
  <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: 12, padding: "18px 20px", ...style }}>
    {title && <p style={{ fontSize: 14, fontWeight: 500, color: "var(--color-text-primary)", marginBottom: 2 }}>{title}</p>}
    {sub && <p style={{ fontSize: 12, color: "var(--color-text-secondary)", marginBottom: 14 }}>{sub}</p>}
    {children}
  </div>
);

// ─── MAIN DASHBOARD ──────────────────────────────────────────────────────
export default function Dashboard() {
  const [selectedYear, setSelectedYear] = useState(2020);
  const [sortCol, setSortCol] = useState("enrollment");
  const [sortAsc, setSortAsc] = useState(false);

  const yearData = useMemo(() => overviewRaw.filter(r => r.year === selectedYear), [selectedYear]);

  // Top 10 provinces by enrollment (exclude aggregates)
  const top10 = useMemo(() =>
    [...yearData].sort((a, b) => b.enrollment - a.enrollment).slice(0, 10)
      .map(r => ({ name: r.province.replace("Banteay Meanchey", "B.Meanchey").replace("Kampong Cham", "K.Cham").replace("Kampong Chhnang", "K.Chhnang").replace("Kampong Speu", "K.Speu").replace("Preah Sihanouk", "Sihanoukville"), enrollment: r.enrollment, enrollF: r.enrollF, schools: r.schools })),
    [yearData]);

  // Province table
  const tableData = useMemo(() => {
    const sorted = [...yearData].sort((a, b) => {
      const va = a[sortCol], vb = b[sortCol];
      return sortAsc ? va - vb : vb - va;
    });
    return sorted;
  }, [yearData, sortCol, sortAsc]);

  // Staff qualifications for selected year
  const staffData = useMemo(() => staffQual.filter(s => s.year === (selectedYear === 2019 ? 2018 : selectedYear)), [selectedYear]);

  // National totals for trend chart
  const trendData = nationalTotals;

  // Gender pie
  const nat = useMemo(() => {
    const tot = yearData.reduce((a, r) => a + r.enrollment, 0);
    const totF = yearData.reduce((a, r) => a + r.enrollF, 0);
    return { total: tot, female: totF, male: tot - totF };
  }, [yearData]);

  // Facility icons
  const facIcons = { Computer:"💻", Printer:"🖨️", LCD_Projector:"📽️", Photocopy:"📠", Library:"📚", Resource_Center:"🗂️", Drinking_Water:"💧", Toilet:"🚻", Health_Room:"🏥", Computer_Room:"🖥️" };
  const facData = facilities[selectedYear === 2019 ? 2020 : selectedYear];

  const handleSort = (col) => {
    if (sortCol === col) setSortAsc(!sortAsc);
    else { setSortCol(col); setSortAsc(false); }
  };

  const colStyle = (col) => ({ cursor: "pointer", color: sortCol === col ? COLORS.amber : "var(--color-text-secondary)", fontWeight: sortCol === col ? 500 : 400 });

  return (
    <div style={{ fontFamily: "var(--font-sans)", padding: "24px 28px", maxWidth: 1100, margin: "0 auto" }}>

      {/* HEADER */}
      <div style={{ marginBottom: 28, display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 16 }}>
        <div>
          <p style={{ fontSize: 11, fontWeight: 500, letterSpacing: "0.12em", textTransform: "uppercase", color: COLORS.amber, marginBottom: 6 }}>Cambodia · Ministry of Education</p>
          <h1 style={{ fontSize: 26, fontWeight: 500, color: "var(--color-text-primary)", marginBottom: 4 }}>Private Schools Dashboard</h1>
          <p style={{ fontSize: 13, color: "var(--color-text-secondary)" }}>Academic years 2018–19, 2019–20, 2020–21 · 25 provinces</p>
        </div>
        <div style={{ display: "flex", gap: 6 }}>
          {[2018, 2019, 2020].map(y => (
            <button key={y} onClick={() => setSelectedYear(y)}
              style={{ padding: "7px 18px", borderRadius: 8, border: `0.5px solid ${selectedYear === y ? COLORS.amber : "var(--color-border-secondary)"}`,
                background: selectedYear === y ? COLORS.amber : "var(--color-background-secondary)",
                color: selectedYear === y ? "#1a1a1a" : "var(--color-text-secondary)", fontWeight: selectedYear === y ? 500 : 400, fontSize: 13, cursor: "pointer" }}>
              {y}–{y - 1999}
            </button>
          ))}
        </div>
      </div>

      {/* KPI GRID */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(155px, 1fr))", gap: 12, marginBottom: 28 }}>
        <StatCard label="Total Schools"    value={yearData.reduce((a,r)=>a+r.schools,0).toLocaleString()}     color={COLORS.blue}   sub="Private schools nationwide" />
        <StatCard label="Total Enrollment" value={nat.total.toLocaleString()}                                  color={COLORS.teal}   sub={`${pct(nat.female, nat.total)} female`} />
        <StatCard label="Teaching Staff"   value={yearData.reduce((a,r)=>a+r.teachStaff,0).toLocaleString()}  color={COLORS.amber}  sub="Incl. foreign teachers" />
        <StatCard label="Foreign Teachers" value={yearData.reduce((a,r)=>a+r.foreignTeach,0).toLocaleString()} color={COLORS.purple} sub="International teaching staff" />
        <StatCard label="Classrooms"       value={yearData.reduce((a,r)=>a+r.classrooms,0).toLocaleString()}  color={COLORS.coral}  sub="Across all provinces" />
        <StatCard label="Students / School" value={Math.round(nat.total / Math.max(yearData.reduce((a,r)=>a+r.schools,0),1))} color={COLORS.green} sub="National average" />
      </div>

      {/* ── SECTION 1: ENROLLMENT ─────────────────────────────────────── */}
      <SectionHeader title="🏫 Enrollment & Schools" sub="Top provinces by student count and gender split" />

      <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 16, marginBottom: 16 }}>
        <ChartCard title="Top 10 Provinces by Enrollment" sub="Total vs female students">
          <div style={{ position: "relative", width: "100%", height: 280 }}>
            <ResponsiveContainer>
              <BarChart data={top10} layout="vertical" margin={{ left: 70, right: 20, top: 4, bottom: 4 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-tertiary)" horizontal={false} />
                <XAxis type="number" tickFormatter={fmt} tick={{ fontSize: 11, fill: "var(--color-text-secondary)" }} />
                <YAxis type="category" dataKey="name" tick={{ fontSize: 11, fill: "var(--color-text-secondary)" }} width={68} />
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="enrollment" name="Total" fill={COLORS.blue} radius={[0, 3, 3, 0]} />
                <Bar dataKey="enrollF" name="Female" fill={COLORS.teal} radius={[0, 3, 3, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <ChartCard title="Gender Breakdown" sub="Female share of enrollment">
          <div style={{ position: "relative", width: "100%", height: 200 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie data={[{ name: "Female", value: nat.female }, { name: "Male", value: nat.male }]}
                  cx="50%" cy="50%" outerRadius={80} innerRadius={48} dataKey="value" label={({ name, percent }) => `${name} ${(percent * 100).toFixed(1)}%`}
                  labelLine={false}>
                  <Cell fill={COLORS.teal} />
                  <Cell fill={COLORS.blue} />
                </Pie>
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div style={{ textAlign: "center", fontSize: 13, color: "var(--color-text-secondary)", marginTop: 4 }}>
            {nat.female.toLocaleString()} female · {nat.male.toLocaleString()} male
          </div>
        </ChartCard>
      </div>

      {/* Trend line */}
      <ChartCard title="National Trends Across Three Academic Years" sub="Schools, enrollment, and teaching staff (normalised scale)">
        <div style={{ position: "relative", width: "100%", height: 220 }}>
          <ResponsiveContainer>
            <LineChart data={trendData} margin={{ left: 10, right: 20, top: 8, bottom: 4 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-tertiary)" />
              <XAxis dataKey="year" tick={{ fontSize: 11, fill: "var(--color-text-secondary)" }} />
              <YAxis yAxisId="left" tickFormatter={fmt} tick={{ fontSize: 11, fill: "var(--color-text-secondary)" }} />
              <YAxis yAxisId="right" orientation="right" tickFormatter={fmt} tick={{ fontSize: 11, fill: "var(--color-text-secondary)" }} />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Line yAxisId="right" type="monotone" dataKey="schools" name="Schools" stroke={COLORS.purple} strokeWidth={2} dot={{ r: 4 }} />
              <Line yAxisId="left" type="monotone" dataKey="enrollment" name="Enrollment" stroke={COLORS.blue} strokeWidth={2} dot={{ r: 4 }} />
              <Line yAxisId="left" type="monotone" dataKey="teachStaff" name="Teaching Staff" stroke={COLORS.amber} strokeWidth={2} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </ChartCard>

      {/* ── SECTION 2: STAFF ─────────────────────────────────────────── */}
      <SectionHeader title="👩‍🏫 Teaching Staff" sub="Qualification levels, gender parity, and pedagogical training" />

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
        <ChartCard title="Staff by Qualification Level" sub="Total vs female (2018 & 2020 national)">
          <div style={{ position: "relative", width: "100%", height: 240 }}>
            <ResponsiveContainer>
              <BarChart data={staffQual.filter(s => s.year === 2020)} margin={{ left: 10, right: 10, top: 4, bottom: 4 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-tertiary)" />
                <XAxis dataKey="level" tick={{ fontSize: 10, fill: "var(--color-text-secondary)" }} />
                <YAxis tickFormatter={fmt} tick={{ fontSize: 11, fill: "var(--color-text-secondary)" }} />
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="total" name="Total" fill={COLORS.blue} radius={[3, 3, 0, 0]} />
                <Bar dataKey="female" name="Female" fill={COLORS.teal} radius={[3, 3, 0, 0]} />
                <Bar dataKey="noPed" name="No Ped. Training" fill={COLORS.coral} radius={[3, 3, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <ChartCard title="Female Share by Qualification (2020)" sub="% female of total at each qualification level">
          <div style={{ position: "relative", width: "100%", height: 240 }}>
            <ResponsiveContainer>
              <RadarChart data={staffQual.filter(s => s.year === 2020).map(s => ({
                level: s.level,
                femalePct: Math.round((s.female / s.total) * 100),
                noPedPct: Math.round((s.noPed / s.total) * 100)
              }))}>
                <PolarGrid stroke="var(--color-border-tertiary)" />
                <PolarAngleAxis dataKey="level" tick={{ fontSize: 10, fill: "var(--color-text-secondary)" }} />
                <Radar name="% Female" dataKey="femalePct" stroke={COLORS.teal} fill={COLORS.teal} fillOpacity={0.3} />
                <Radar name="% No Ped Training" dataKey="noPedPct" stroke={COLORS.coral} fill={COLORS.coral} fillOpacity={0.2} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Tooltip content={<CustomTooltip />} formatter={(v) => v + "%"} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      {/* ── SECTION 3: REPEATERS ─────────────────────────────────────── */}
      <SectionHeader title="🔁 Grade Repeaters" sub="National total students repeating a grade (2020–21)" />

      <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 16, marginBottom: 16 }}>
        <ChartCard title="Repeaters by Grade (Grades 1–12)" sub="Total vs girls — higher in lower grades">
          <div style={{ position: "relative", width: "100%", height: 240 }}>
            <ResponsiveContainer>
              <BarChart data={repeatersByGrade} margin={{ left: 10, right: 10, top: 4, bottom: 4 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-tertiary)" />
                <XAxis dataKey="grade" tick={{ fontSize: 11, fill: "var(--color-text-secondary)" }} />
                <YAxis tick={{ fontSize: 11, fill: "var(--color-text-secondary)" }} />
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="total" name="Total Repeaters" fill={COLORS.amber} radius={[3, 3, 0, 0]} />
                <Bar dataKey="girls" name="Girls" fill={COLORS.coral} radius={[3, 3, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <ChartCard title="Repeater Rate by Year" sub="National repeaters as % of enrollment">
          <div style={{ position: "relative", width: "100%", height: 240 }}>
            <ResponsiveContainer>
              <BarChart data={[
                { year: "2018–19", rate: parseFloat(((2832/170739)*100).toFixed(2)) },
                { year: "2019–20", rate: parseFloat(((2100/186745)*100).toFixed(2)) },
                { year: "2020–21", rate: parseFloat(((1980/240550)*100).toFixed(2)) },
              ]} margin={{ left: 0, right: 10, top: 4, bottom: 4 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-tertiary)" />
                <XAxis dataKey="year" tick={{ fontSize: 11, fill: "var(--color-text-secondary)" }} />
                <YAxis tickFormatter={v => v + "%"} tick={{ fontSize: 11, fill: "var(--color-text-secondary)" }} />
                <Tooltip content={<CustomTooltip />} formatter={v => v + "%"} />
                <Bar dataKey="rate" name="Repeater rate %" fill={COLORS.purple} radius={[3, 3, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      {/* ── SECTION 4: FACILITIES ────────────────────────────────────── */}
      <SectionHeader title="🖥️ Learning Facilities" sub={`National facility counts · ${selectedYear === 2019 ? "Using 2020 data (closest available)" : selectedYear + "–" + (selectedYear - 1999)}`} />

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(120px, 1fr))", gap: 10, marginBottom: 16 }}>
        {Object.entries(facData).map(([key, val]) => (
          <div key={key} style={{ background: "var(--color-background-secondary)", borderRadius: 10, padding: "14px 12px", textAlign: "center" }}>
            <span style={{ fontSize: 22, display: "block", marginBottom: 6 }}>{facIcons[key] || "📋"}</span>
            <p style={{ fontSize: 18, fontWeight: 500, color: "var(--color-text-primary)" }}>{val.toLocaleString()}</p>
            <p style={{ fontSize: 11, color: "var(--color-text-secondary)", marginTop: 3 }}>{key.replace(/_/g, " ")}</p>
          </div>
        ))}
      </div>

      {/* Urban vs Rural */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
        <ChartCard title="Urban vs Rural Split (2020–21)" sub="Schools, enrollment, and teaching staff">
          <div style={{ position: "relative", width: "100%", height: 220 }}>
            <ResponsiveContainer>
              <BarChart data={urbanRural2020} margin={{ left: 10, right: 10, top: 4, bottom: 4 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-tertiary)" />
                <XAxis dataKey="name" tick={{ fontSize: 12, fill: "var(--color-text-secondary)" }} />
                <YAxis tickFormatter={fmt} tick={{ fontSize: 11, fill: "var(--color-text-secondary)" }} />
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="enrollment" name="Enrollment" fill={COLORS.blue} radius={[3, 3, 0, 0]} />
                <Bar dataKey="teachStaff" name="Teaching Staff" fill={COLORS.amber} radius={[3, 3, 0, 0]} />
                <Bar dataKey="schools" name="Schools" fill={COLORS.teal} radius={[3, 3, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <ChartCard title="Urban vs Rural Share" sub="% of total enrollment and schools">
          <div style={{ position: "relative", width: "100%", height: 220 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie data={urbanRural2020} cx="50%" cy="50%" outerRadius={78} innerRadius={44}
                  dataKey="enrollment" nameKey="name"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`} labelLine={false}>
                  <Cell fill={COLORS.blue} />
                  <Cell fill={COLORS.green} />
                </Pie>
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <p style={{ fontSize: 12, color: "var(--color-text-secondary)", textAlign: "center" }}>
            Urban: {((196707 / 240550) * 100).toFixed(1)}% of enrollment · Rural: {((43843 / 240550) * 100).toFixed(1)}%
          </p>
        </ChartCard>
      </div>

      {/* ── SECTION 5: PROVINCE TABLE ─────────────────────────────────── */}
      <SectionHeader title="📊 Province Rankings" sub={`Click column headers to sort · ${selectedYear}–${selectedYear - 1999} data`} />

      <div style={{ border: "0.5px solid var(--color-border-tertiary)", borderRadius: 12, overflow: "hidden" }}>
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
            <thead>
              <tr style={{ background: "var(--color-background-secondary)", borderBottom: "0.5px solid var(--color-border-secondary)" }}>
                {[
                  ["Province", "province"],
                  ["Schools", "schools"],
                  ["Enrollment", "enrollment"],
                  ["% Female", null],
                  ["Teachers", "teachStaff"],
                  ["Foreign", "foreignTeach"],
                  ["Classrooms", "classrooms"],
                  ["Stu/School", null],
                ].map(([label, col]) => (
                  <th key={label} onClick={col ? () => handleSort(col) : undefined}
                    style={{ padding: "10px 14px", textAlign: "left", fontSize: 11, textTransform: "uppercase", letterSpacing: "0.07em", ...colStyle(col), whiteSpace: "nowrap", userSelect: "none" }}>
                    {label} {col && sortCol === col ? (sortAsc ? "↑" : "↓") : col ? "↕" : ""}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {tableData.map((r, i) => (
                <tr key={r.province} style={{ borderBottom: "0.5px solid var(--color-border-tertiary)", background: i % 2 === 0 ? "transparent" : "var(--color-background-secondary)" }}>
                  <td style={{ padding: "9px 14px", fontWeight: 500, color: "var(--color-text-primary)", whiteSpace: "nowrap" }}>{r.province}</td>
                  <td style={{ padding: "9px 14px", color: "var(--color-text-primary)" }}>{r.schools}</td>
                  <td style={{ padding: "9px 14px", color: "var(--color-text-primary)" }}>{r.enrollment.toLocaleString()}</td>
                  <td style={{ padding: "9px 14px" }}>
                    <span style={{ background: "var(--color-background-info)", color: "var(--color-text-info)", padding: "2px 8px", borderRadius: 20, fontSize: 11, fontWeight: 500 }}>
                      {pct(r.enrollF, r.enrollment)}
                    </span>
                  </td>
                  <td style={{ padding: "9px 14px", color: "var(--color-text-primary)" }}>{r.teachStaff.toLocaleString()}</td>
                  <td style={{ padding: "9px 14px", color: "var(--color-text-secondary)" }}>{r.foreignTeach}</td>
                  <td style={{ padding: "9px 14px", color: "var(--color-text-primary)" }}>{r.classrooms.toLocaleString()}</td>
                  <td style={{ padding: "9px 14px", color: "var(--color-text-secondary)" }}>{Math.round(r.enrollment / Math.max(r.schools, 1))}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* FOOTER */}
      <p style={{ fontSize: 11, color: "var(--color-text-secondary)", textAlign: "center", marginTop: 32 }}>
        Data source: Cambodia Ministry of Education, Youth and Sport · Private Schools Statistics 2018–19, 2019–20, 2020–21
      </p>
    </div>
  );
}
