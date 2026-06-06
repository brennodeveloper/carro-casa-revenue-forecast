  import { useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface ForecastItem {
  month: string;
  scenario: string;
  predicted_revenue: number;
}

interface ForecastResponse {
  message: string;
  forecast: ForecastItem[];
}

interface ChartData {
  month: string;
  Conservative?: number;
  Expected?: number;
  Optimistic?: number;
  [key: string]: string | number | undefined;
}

const API_URL = "https://carro-casa-revenue-forecast.onrender.com/api/forecast";

const SCENARIO_COLORS: Record<string, string> = {
  Conservative: "#f59e0b",
  Expected: "#3b82f6",
  Optimistic: "#10b981",
};

const formatCurrency = (value: number) =>
  new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
    maximumFractionDigits: 0,
  }).format(value);

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<ForecastResponse | null>(null);

  const handleSubmit = async () => {
    if (!file) {
      setError("Selecione uma planilha Excel ou CSV primeiro.");
      return;
    }
    
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post<ForecastResponse>(API_URL, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setData(response.data);
    } catch (error) {
      const requestError = error as {
        response?: {
          data?: {
            error?: string;
            message?: string;
            details?: string;
          };
        };
        message?: string;
      };

      setError(
        requestError.response?.data?.error ||
          requestError.response?.data?.message ||
          requestError.response?.data?.details ||
          requestError.message ||
          "Erro ao gerar previsão. Tente novamente.",
      );
    } finally {
      setLoading(false);
    }
  };

  const chartData: ChartData[] = (() => {
    if (!data) return [];

    const map = new Map<string, ChartData>();

    for (const item of data.forecast) {
      const row = map.get(item.month) ?? { month: item.month };

      row[item.scenario] = item.predicted_revenue;

      map.set(item.month, row);
    }

    return Array.from(map.values());
  })();

  const scenarios = data
    ? Array.from(new Set(data.forecast.map((item) => item.scenario)))
    : [];

  const stats = (() => {
    if (!data || data.forecast.length === 0) return null;

    const revenues = data.forecast.map((item) => item.predicted_revenue);
    const min = Math.min(...revenues);
    const max = Math.max(...revenues);

    const expectedForecast = data.forecast.filter(
      (item) => item.scenario === "Expected",
    );

    const avgExpected =
      expectedForecast.length > 0
        ? expectedForecast.reduce(
            (sum, item) => sum + item.predicted_revenue,
            0,
          ) / expectedForecast.length
        : 0;

    return {
      min,
      max,
      avgExpected,
    };
  })();

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <header className="mb-10">
          <h1 className="text-4xl font-bold tracking-tight">
            Previsão de Faturamento
          </h1>
          <p className="mt-2 text-muted-foreground">
            Faça upload de uma planilha Excel ou CSV para gerar projeções de faturamento
            por cenário.
          </p>
        </header>

        <section className="mb-8 rounded-xl border border-border bg-card/40 p-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
            <label className="flex-1 cursor-pointer">
              <input
                type="file"
                accept=".xlsx,.csv"
                onChange={(event) => setFile(event.target.files?.[0] ?? null)}
                className="block w-full text-sm text-foreground file:mr-4 file:rounded-md file:border-0 file:bg-primary file:px-4 file:py-2 file:text-sm file:font-medium file:text-primary-foreground hover:file:bg-primary/90"
              />

              {file && (
                <span className="mt-2 block text-xs text-muted-foreground">
                  {file.name}
                </span>
              )}
            </label>

            <button
              onClick={handleSubmit}
              disabled={loading || !file}
              className="rounded-md bg-primary px-6 py-2.5 font-medium text-primary-foreground transition-colors hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Gerando..." : "Gerar previsão"}
            </button>
          </div>

          {error && (
            <div className="mt-4 rounded-md border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm text-destructive-foreground">
              {error}
            </div>
          )}

          {loading && (
            <div className="mt-4 text-sm text-muted-foreground">
              Processando a planilha e gerando cenários...
            </div>
          )}

          {data?.message && !loading && (
            <div className="mt-4 text-sm text-muted-foreground">
              {data.message}
            </div>
          )}
        </section>

        {stats && (
          <section className="mb-8 grid gap-4 sm:grid-cols-3">
            <StatCard
              label="Menor previsão"
              value={formatCurrency(stats.min)}
              accent="#f59e0b"
            />

            <StatCard
              label="Previsão esperada média"
              value={formatCurrency(stats.avgExpected)}
              accent="#3b82f6"
            />

            <StatCard
              label="Maior previsão"
              value={formatCurrency(stats.max)}
              accent="#10b981"
            />
          </section>
        )}

        {data && chartData.length > 0 && (
          <section className="mb-8 rounded-xl border border-border bg-card/40 p-6">
            <h2 className="mb-4 text-lg font-semibold">Cenários por mês</h2>

            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#ffffff15" />

                  <XAxis dataKey="month" stroke="#94a3b8" />

                  <YAxis
                    stroke="#94a3b8"
                    tickFormatter={(value) =>
                      `R$ ${(Number(value) / 1000).toFixed(0)}k`
                    }
                  />

                  <Tooltip
                    contentStyle={{
                      background: "#0f172a",
                      border: "1px solid #334155",
                      borderRadius: 8,
                    }}
                    formatter={(value) => formatCurrency(Number(value))}
                  />

                  <Legend />

                  {scenarios.map((scenario) => (
                    <Line
                      key={scenario}
                      type="monotone"
                      dataKey={scenario}
                      stroke={SCENARIO_COLORS[scenario] ?? "#a78bfa"}
                      strokeWidth={2.5}
                      dot={{ r: 3 }}
                      activeDot={{ r: 5 }}
                    />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            </div>
          </section>
        )}

        {data && data.forecast.length > 0 && (
          <section className="rounded-xl border border-border bg-card/40 p-6">
            <h2 className="mb-4 text-lg font-semibold">Detalhamento</h2>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="border-b border-border text-muted-foreground">
                  <tr>
                    <th className="px-3 py-2 font-medium">Mês</th>
                    <th className="px-3 py-2 font-medium">Cenário</th>
                    <th className="px-3 py-2 text-right font-medium">
                      Faturamento previsto
                    </th>
                  </tr>
                </thead>

                <tbody>
                  {data.forecast.map((row, index) => (
                    <tr
                      key={`${row.month}-${row.scenario}-${index}`}
                      className="border-b border-border/50 last:border-0"
                    >
                      <td className="px-3 py-2">{row.month}</td>

                      <td className="px-3 py-2">
                        <span
                          className="inline-flex items-center gap-2 rounded-full px-2.5 py-0.5 text-xs font-medium"
                          style={{
                            background: `${
                              SCENARIO_COLORS[row.scenario] ?? "#a78bfa"
                            }22`,
                            color: SCENARIO_COLORS[row.scenario] ?? "#a78bfa",
                          }}
                        >
                          {row.scenario}
                        </span>
                      </td>

                      <td className="px-3 py-2 text-right font-mono">
                        {formatCurrency(row.predicted_revenue)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}
      </div>
    </div>
  );
}

function StatCard({
  label,
  value,
  accent,
}: {
  label: string;
  value: string;
  accent: string;
}) {
  return (
    <div className="rounded-xl border border-border bg-card/40 p-5">
      <div
        className="mb-2 inline-block h-1 w-10 rounded-full"
        style={{ background: accent }}
      />

      <div className="text-sm text-muted-foreground">{label}</div>

      <div className="mt-1 text-2xl font-semibold tracking-tight">{value}</div>
    </div>
  );
}