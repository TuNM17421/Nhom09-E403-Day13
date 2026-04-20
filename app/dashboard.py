from __future__ import annotations


def render_dashboard_html() -> str:
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Day 13 Observability Dashboard</title>
  <style>
    :root {
      --bg: #0b1220;
      --panel: #111a2e;
      --panel-border: #26324d;
      --text: #e8eefc;
      --muted: #9eb0d1;
      --good: #22c55e;
      --warn: #f59e0b;
      --bad: #ef4444;
      --accent: #60a5fa;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: Segoe UI, Arial, sans-serif;
      background: linear-gradient(180deg, #08101d 0%, #0b1220 100%);
      color: var(--text);
    }

    .container {
      max-width: 1280px;
      margin: 0 auto;
      padding: 24px;
    }

    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      margin-bottom: 20px;
    }

    .title h1 {
      margin: 0 0 8px;
      font-size: 28px;
    }

    .title p,
    .meta {
      margin: 0;
      color: var(--muted);
    }

    .meta {
      text-align: right;
      font-size: 14px;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
    }

    .card {
      background: rgba(17, 26, 46, 0.95);
      border: 1px solid var(--panel-border);
      border-radius: 16px;
      padding: 18px;
      min-height: 170px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
    }

    .card h2 {
      font-size: 16px;
      margin: 0 0 12px;
      color: #dbe7ff;
    }

    .value {
      font-size: 30px;
      font-weight: 700;
      margin-bottom: 8px;
    }

    .sub {
      color: var(--muted);
      font-size: 14px;
      line-height: 1.4;
      white-space: pre-line;
    }

    .pill {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 600;
      margin-top: 10px;
    }

    .good { background: rgba(34, 197, 94, 0.15); color: #86efac; }
    .warn { background: rgba(245, 158, 11, 0.15); color: #fcd34d; }
    .bad { background: rgba(239, 68, 68, 0.15); color: #fca5a5; }

    .footer {
      margin-top: 18px;
      color: var(--muted);
      font-size: 13px;
    }

    @media (max-width: 960px) {
      .grid { grid-template-columns: 1fr; }
      .header { flex-direction: column; align-items: flex-start; }
      .meta { text-align: left; }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="title">
        <h1>Day 13 Observability Dashboard</h1>
        <p>Live dashboard for the final demo, refreshed every 15 seconds.</p>
      </div>
      <div class="meta">
        <div>Window: Last 1 hour</div>
        <div id="meta-status">Loading live metrics...</div>
      </div>
    </div>

    <div class="grid">
      <div class="card">
        <h2>Latency P50 P95 P99</h2>
        <div class="value" id="latency-value">--</div>
        <div class="sub" id="latency-sub">Threshold: P95 &lt; 2000 ms</div>
        <span class="pill good" id="latency-pill">Waiting</span>
      </div>

      <div class="card">
        <h2>Traffic QPS</h2>
        <div class="value" id="qps-value">--</div>
        <div class="sub" id="qps-sub">Requests per second based on live traffic deltas.</div>
        <span class="pill good" id="qps-pill">Waiting</span>
      </div>

      <div class="card">
        <h2>Error Rate Percent</h2>
        <div class="value" id="error-value">--</div>
        <div class="sub" id="error-sub">Threshold: Error rate &lt; 1%</div>
        <span class="pill good" id="error-pill">Waiting</span>
      </div>

      <div class="card">
        <h2>Cost Dollars per Hour</h2>
        <div class="value" id="cost-value">--</div>
        <div class="sub" id="cost-sub">Alert threshold: 0.5 USD/hour</div>
        <span class="pill good" id="cost-pill">Waiting</span>
      </div>

      <div class="card">
        <h2>Tokens In and Out</h2>
        <div class="value" id="tokens-value">--</div>
        <div class="sub" id="tokens-sub">Live token usage totals for prompt and answer flows.</div>
        <span class="pill good" id="tokens-pill">Waiting</span>
      </div>

      <div class="card">
        <h2>Hallucination Percent</h2>
        <div class="value" id="hallucination-value">--</div>
        <div class="sub" id="hallucination-sub">Derived from 100 × (1 - quality score average)</div>
        <span class="pill good" id="hallucination-pill">Waiting</span>
      </div>
    </div>

    <div class="footer">
      Use the chat endpoint or load test script to generate traffic before taking the final screenshot.
    </div>
  </div>

  <script>
    let lastTraffic = null;
    let lastCost = null;
    let lastTimestamp = null;

    function setCard(id, value, sub, status, tone) {
      document.getElementById(id + '-value').textContent = value;
      document.getElementById(id + '-sub').textContent = sub;
      const pill = document.getElementById(id + '-pill');
      pill.textContent = status;
      pill.className = 'pill ' + tone;
    }

    function formatNumber(value, digits = 2) {
      return Number(value || 0).toFixed(digits);
    }

    async function refreshDashboard() {
      try {
        const [metricsResp, healthResp] = await Promise.all([
          fetch('/metrics'),
          fetch('/health')
        ]);

        const metrics = await metricsResp.json();
        const health = await healthResp.json();
        const now = Date.now();

        const totalErrors = Object.values(metrics.error_breakdown || {}).reduce((sum, item) => sum + item, 0);
        const errorRate = metrics.traffic > 0 ? (totalErrors / metrics.traffic) * 100 : 0;
        const hallucinationPct = (1 - (metrics.quality_avg || 0)) * 100;

        let qps = 0;
        let hourlyCost = 0;
        if (lastTimestamp !== null) {
          const seconds = (now - lastTimestamp) / 1000;
          if (seconds > 0) {
            qps = ((metrics.traffic || 0) - (lastTraffic || 0)) / seconds;
            hourlyCost = (((metrics.total_cost_usd || 0) - (lastCost || 0)) / seconds) * 3600;
          }
        }

        lastTraffic = metrics.traffic || 0;
        lastCost = metrics.total_cost_usd || 0;
        lastTimestamp = now;

        setCard(
          'latency',
          'P50 ' + formatNumber(metrics.latency_p50, 0) + ' | P95 ' + formatNumber(metrics.latency_p95, 0) + ' | P99 ' + formatNumber(metrics.latency_p99, 0),
          'SLO target: P95 under 2000 ms',
          metrics.latency_p95 > 2000 ? 'Above SLO' : 'Healthy',
          metrics.latency_p95 > 2000 ? 'bad' : 'good'
        );

        setCard(
          'qps',
          formatNumber(qps, 2) + ' qps',
          'Total traffic: ' + (metrics.traffic || 0) + ' requests',
          qps > 0 ? 'Active traffic' : 'Idle or low load',
          qps > 0 ? 'good' : 'warn'
        );

        setCard(
          'error',
          formatNumber(errorRate, 2) + '%',
          'Errors: ' + totalErrors + ' across ' + (metrics.traffic || 0) + ' requests',
          errorRate > 1 ? 'Investigate now' : 'Within target',
          errorRate > 1 ? 'bad' : 'good'
        );

        setCard(
          'cost',
          '$' + formatNumber(hourlyCost, 4) + '/hour',
          'Total cost so far: $' + formatNumber(metrics.total_cost_usd, 4),
          hourlyCost > 0.5 ? 'Burn spike' : 'Budget okay',
          hourlyCost > 0.5 ? 'warn' : 'good'
        );

        setCard(
          'tokens',
          'In ' + (metrics.tokens_in_total || 0) + ' | Out ' + (metrics.tokens_out_total || 0),
          'Tracks prompt and response token usage live',
          (metrics.tokens_in_total || 0) + (metrics.tokens_out_total || 0) > 0 ? 'Live usage' : 'No requests yet',
          'good'
        );

        setCard(
          'hallucination',
          formatNumber(hallucinationPct, 2) + '%',
          'Quality avg: ' + formatNumber(metrics.quality_avg || 0, 2),
          hallucinationPct > 25 ? 'Watch quality' : 'Quality stable',
          hallucinationPct > 25 ? 'warn' : 'good'
        );

        document.getElementById('meta-status').textContent = 'Health: ' + (health.ok ? 'OK' : 'Issue') + ' | Tracing: ' + (health.tracing_enabled ? 'On' : 'Off');
      } catch (error) {
        document.getElementById('meta-status').textContent = 'Dashboard refresh failed';
        console.error(error);
      }
    }

    refreshDashboard();
    setInterval(refreshDashboard, 15000);
  </script>
</body>
</html>
"""
