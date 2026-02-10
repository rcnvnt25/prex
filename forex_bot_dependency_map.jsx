import React, { useState } from 'react';
import { ChevronDown, ChevronRight, AlertCircle, CheckCircle, Database, Cloud, Zap, Lock } from 'lucide-react';

const DependencyMap = () => {
  const [expandedNodes, setExpandedNodes] = useState({
    core: true,
    mt5: true,
    news: true,
    trading: true,
    config: true,
    monitoring: true
  });

  const toggleNode = (nodeId) => {
    setExpandedNodes(prev => ({ ...prev, [nodeId]: !prev[nodeId] }));
  };

  const dependencies = {
    core: {
      title: "🤖 Core System",
      color: "bg-blue-500",
      items: [
        { name: "forex_ai_bot.py", type: "main", deps: ["NewsAnalyzer", "ForexAIBot", "MT5 Connection"] },
        { name: "Python 3.8+", type: "runtime", deps: [] },
        { name: "requirements.txt", type: "config", deps: ["All Python packages"] }
      ]
    },
    mt5: {
      title: "📊 MetaTrader 5 Integration",
      color: "bg-green-500",
      items: [
        { name: "MetaTrader5 >= 5.0.45", type: "package", deps: [] },
        { name: "MT5 Terminal", type: "external", deps: ["Must be running"] },
        { name: ".env Configuration", type: "config", deps: ["MT5_LOGIN", "MT5_PASSWORD", "MT5_SERVER"] },
        { name: "Demo Account", type: "account", deps: ["Broker credentials"] }
      ]
    },
    news: {
      title: "📰 News Sources",
      color: "bg-purple-500",
      items: [
        { name: "Telegram: @marketfeed", type: "external", deps: ["Telegram Bot API"] },
        { name: "Telegram: @wfwitness", type: "external", deps: ["Telegram Bot API"] },
        { name: "NewsAnalyzer Class", type: "module", deps: ["Sentiment keywords", "AI analysis"] },
        { name: "Real-time News Fetcher", type: "service", deps: ["API credentials"] }
      ]
    },
    trading: {
      title: "💹 Trading Logic",
      color: "bg-orange-500",
      items: [
        { name: "Multi-pair Support", type: "feature", deps: ["All forex pairs"] },
        { name: "Auto Position Opening", type: "feature", deps: ["News sentiment"] },
        { name: "Risk Management", type: "module", deps: ["SL: 1%", "TP: 10%"] },
        { name: "Position Monitor", type: "service", deps: ["Real-time tracking"] }
      ]
    },
    config: {
      title: "⚙️ Configuration",
      color: "bg-yellow-500",
      items: [
        { name: "advanced_config.py", type: "file", deps: ["Trading strategies"] },
        { name: ".env file", type: "file", deps: ["Secrets & credentials"] },
        { name: "Broker Settings", type: "config", deps: ["Broker-specific params"] },
        { name: "Daily Limits", type: "config", deps: ["Circuit breaker rules"] }
      ]
    },
    monitoring: {
      title: "📈 Monitoring & Backtest",
      color: "bg-red-500",
      items: [
        { name: "backtest_monitor.py", type: "file", deps: ["TradingMonitor", "BacktestEngine"] },
        { name: "Performance Stats", type: "feature", deps: ["Win rate", "Profit factor"] },
        { name: "Trading Log", type: "storage", deps: ["trading_log.json"] },
        { name: "Daily Summary", type: "report", deps: ["Trade history"] }
      ]
    }
  };

  const dataFlows = [
    { from: "Telegram News", to: "NewsAnalyzer", label: "Raw news" },
    { from: "NewsAnalyzer", to: "Sentiment Score", label: "Analysis" },
    { from: "Sentiment Score", to: "Trading Signal", label: "BUY/SELL" },
    { from: "Trading Signal", to: "MT5", label: "Execute order" },
    { from: "MT5", to: "Monitor", label: "Position data" },
    { from: ".env", to: "MT5 Connection", label: "Credentials" }
  ];

  const DependencyNode = ({ category, data }) => {
    const isExpanded = expandedNodes[category];
    const colorClass = data.color;

    return (
      <div className="mb-4 border-2 border-gray-300 rounded-lg overflow-hidden shadow-lg">
        <div 
          className={`${colorClass} text-white p-4 flex items-center justify-between cursor-pointer hover:opacity-90 transition-opacity`}
          onClick={() => toggleNode(category)}
        >
          <div className="flex items-center gap-2">
            {isExpanded ? <ChevronDown size={20} /> : <ChevronRight size={20} />}
            <h3 className="font-bold text-lg">{data.title}</h3>
          </div>
          <span className="bg-white bg-opacity-20 px-3 py-1 rounded-full text-sm">
            {data.items.length} items
          </span>
        </div>
        
        {isExpanded && (
          <div className="bg-white p-4">
            {data.items.map((item, idx) => (
              <div key={idx} className="mb-3 p-3 bg-gray-50 rounded-lg border border-gray-200">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="font-semibold text-gray-800 flex items-center gap-2">
                      {item.type === 'external' && <Cloud size={16} className="text-blue-500" />}
                      {item.type === 'config' && <Lock size={16} className="text-yellow-500" />}
                      {item.type === 'feature' && <Zap size={16} className="text-orange-500" />}
                      {item.type === 'storage' && <Database size={16} className="text-green-500" />}
                      {item.name}
                    </div>
                    <div className="text-sm text-gray-600 mt-1">
                      <span className="bg-gray-200 px-2 py-0.5 rounded text-xs mr-2">
                        {item.type}
                      </span>
                      {item.deps.length > 0 && (
                        <span className="text-xs">
                          Depends on: {item.deps.join(', ')}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  const EnvExample = () => (
    <div className="mt-6 p-6 bg-gray-900 text-green-400 rounded-lg font-mono text-sm">
      <div className="flex items-center gap-2 mb-3 text-white">
        <Lock size={20} />
        <h4 className="font-bold">.env File Structure</h4>
      </div>
      <pre className="whitespace-pre-wrap">
{`# MetaTrader 5 Account Configuration
MT5_LOGIN=12345678
MT5_PASSWORD=YourPassword123
MT5_SERVER=BrokerName-Demo
MT5_PATH=C:\\Program Files\\MetaTrader 5\\terminal64.exe

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# News API Keys (Optional)
NEWS_API_KEY=your_newsapi_key_here
ALPHA_VANTAGE_KEY=your_alphavantage_key_here

# Trading Configuration
DEFAULT_LOT_SIZE=0.01
STOP_LOSS_PERCENT=1.0
TAKE_PROFIT_PERCENT=10.0
CHECK_INTERVAL=60

# Risk Management
MAX_DAILY_LOSS=50.0
MAX_DAILY_PROFIT=200.0
MAX_TRADES_PER_DAY=10
MAX_CONSECUTIVE_LOSSES=3

# Environment
ENVIRONMENT=demo  # demo or live`}
      </pre>
    </div>
  );

  const DataFlowDiagram = () => (
    <div className="mt-6 p-6 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg">
      <h3 className="font-bold text-xl mb-4 flex items-center gap-2">
        <Zap className="text-orange-500" />
        Data Flow Architecture
      </h3>
      <div className="space-y-3">
        {dataFlows.map((flow, idx) => (
          <div key={idx} className="flex items-center gap-3 p-3 bg-white rounded-lg shadow">
            <div className="bg-blue-100 px-3 py-2 rounded font-semibold text-sm text-blue-800 flex-1">
              {flow.from}
            </div>
            <div className="flex flex-col items-center">
              <div className="text-xs text-gray-600 mb-1">{flow.label}</div>
              <div className="text-2xl text-gray-400">→</div>
            </div>
            <div className="bg-green-100 px-3 py-2 rounded font-semibold text-sm text-green-800 flex-1">
              {flow.to}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const MT5LoginSteps = () => (
    <div className="mt-6 p-6 bg-blue-50 rounded-lg border-2 border-blue-200">
      <h3 className="font-bold text-xl mb-4 flex items-center gap-2">
        <CheckCircle className="text-blue-600" />
        Cara Memasukkan Akun MT5 ke Bot
      </h3>
      <div className="space-y-4">
        <div className="bg-white p-4 rounded-lg shadow">
          <h4 className="font-semibold text-blue-800 mb-2">1️⃣ Buka MT5 Terminal</h4>
          <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
            <li>Login ke akun demo MT5 Anda</li>
            <li>Catat: Login ID, Password, dan Server name</li>
          </ul>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <h4 className="font-semibold text-blue-800 mb-2">2️⃣ Buat File .env</h4>
          <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
            <li>Buat file bernama <code className="bg-gray-200 px-2 py-1 rounded">.env</code> di folder project</li>
            <li>Copy template di bawah dan isi dengan data MT5 Anda</li>
          </ul>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <h4 className="font-semibold text-blue-800 mb-2">3️⃣ Install python-dotenv</h4>
          <code className="block bg-gray-900 text-green-400 p-3 rounded text-sm">
            pip install python-dotenv
          </code>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <h4 className="font-semibold text-blue-800 mb-2">4️⃣ Update Bot Code</h4>
          <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
            <li>Import dotenv di awal file</li>
            <li>Load credentials dari .env</li>
            <li>Pass ke MT5 login function</li>
          </ul>
        </div>
      </div>
    </div>
  );

  const RequiredPackages = () => (
    <div className="mt-6 p-6 bg-green-50 rounded-lg border-2 border-green-200">
      <h3 className="font-bold text-xl mb-4 flex items-center gap-2">
        <Database className="text-green-600" />
        Required Python Packages
      </h3>
      <div className="grid grid-cols-2 gap-3">
        {[
          { pkg: 'MetaTrader5>=5.0.45', purpose: 'MT5 integration' },
          { pkg: 'pandas>=2.0.0', purpose: 'Data manipulation' },
          { pkg: 'numpy>=1.24.0', purpose: 'Numerical computing' },
          { pkg: 'requests>=2.31.0', purpose: 'HTTP requests' },
          { pkg: 'python-dotenv>=1.0.0', purpose: 'Environment variables' },
          { pkg: 'python-telegram-bot>=20.0', purpose: 'Telegram integration' }
        ].map((item, idx) => (
          <div key={idx} className="bg-white p-3 rounded shadow">
            <div className="font-semibold text-sm text-green-800">{item.pkg}</div>
            <div className="text-xs text-gray-600 mt-1">{item.purpose}</div>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto p-6 bg-gradient-to-br from-gray-50 to-blue-50 min-h-screen">
      <div className="bg-white rounded-xl shadow-2xl p-8 mb-6">
        <h1 className="text-4xl font-bold text-center mb-2 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          Forex AI Bot - Dependency Map
        </h1>
        <p className="text-center text-gray-600 mb-6">
          Multi-pair trading dengan Telegram news integration & Demo account
        </p>
        
        <div className="flex gap-4 justify-center mb-8 flex-wrap">
          <span className="bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-semibold">
            ✅ Multi-pair Support
          </span>
          <span className="bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-semibold">
            ✅ Telegram News
          </span>
          <span className="bg-purple-100 text-purple-800 px-4 py-2 rounded-full text-sm font-semibold">
            ✅ Auto Trading
          </span>
          <span className="bg-orange-100 text-orange-800 px-4 py-2 rounded-full text-sm font-semibold">
            ✅ Demo Account
          </span>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-xl p-6 mb-6">
        <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center gap-2">
          <AlertCircle className="text-blue-600" />
          System Components
        </h2>
        {Object.entries(dependencies).map(([key, data]) => (
          <DependencyNode key={key} category={key} data={data} />
        ))}
      </div>

      <div className="bg-white rounded-xl shadow-xl p-6 mb-6">
        <DataFlowDiagram />
      </div>

      <div className="bg-white rounded-xl shadow-xl p-6 mb-6">
        <MT5LoginSteps />
      </div>

      <div className="bg-white rounded-xl shadow-xl p-6 mb-6">
        <EnvExample />
      </div>

      <div className="bg-white rounded-xl shadow-xl p-6 mb-6">
        <RequiredPackages />
      </div>

      <div className="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-xl p-6 border-2 border-yellow-300">
        <div className="flex items-start gap-3">
          <AlertCircle className="text-yellow-600 flex-shrink-0 mt-1" size={24} />
          <div>
            <h3 className="font-bold text-lg text-yellow-900 mb-2">⚠️ Upgrade Summary</h3>
            <ul className="space-y-2 text-sm text-yellow-800">
              <li>✅ <strong>Multi-pair:</strong> Bot akan trade SEMUA pairs yang tersedia di broker</li>
              <li>✅ <strong>Telegram News:</strong> Ambil news dari @marketfeed dan @wfwitness</li>
              <li>✅ <strong>Auto Open:</strong> Bad news = SHORT, Good news = LONG</li>
              <li>✅ <strong>Multi Position:</strong> Bot bisa buka multiple positions secara bersamaan</li>
              <li>✅ <strong>Demo Account:</strong> Testing aman dengan akun demo dulu</li>
              <li>✅ <strong>.env Config:</strong> Credentials tersimpan aman di .env file</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DependencyMap;
