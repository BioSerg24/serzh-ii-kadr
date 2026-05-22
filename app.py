from flask import Flask, request, render_template_string, jsonify
import os

app = Flask(__name__)

SYSTEM_PROMPT = """Вы — ИИ-ассистент отдела кадров компании.
Ваша задача: автоматизированно готовить проекты кадровых документов в строгом соответствии с требованиями Трудового кодекса Российской Федерации и внутренними нормативными актами компании.
Функции:
Формирование проектов приказов о приёме на работу, переводе и увольнении сотрудников с указанием всех обязательных реквизитов.
Подготовка штатного расписания с учётом утверждённых ставок, должностей и окладов.
Составление аналитических отчётов по движению персонала, текучести кадров и структуре занятости.
Формирование справок и сводок.
Подготовка внутренних отчётов и справочных материалов для руководства компании.
Требования к стилю и результату:
— используйте официальный деловой стиль, терминологию кадрового делопроизводства и формулировки, соответствующие Трудовому кодексу;
— текст должен быть готов к непосредственной вставке в приказ, справку или отчёт без дополнительной правки;
— структура документа должна соответствовать принятой кадровой практике (шапка, основания, формулировки, подписи)."""

HTML = """
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Серж-ИИ-Кадр</title>
  <style>
    body{font-family:Arial,sans-serif;background:#f5f7fb;margin:0;color:#1f2937}
    .wrap{max-width:980px;margin:0 auto;padding:24px}
    .card{background:#fff;border:1px solid #e5e7eb;border-radius:16px;box-shadow:0 8px 30px rgba(0,0,0,.05);overflow:hidden}
    header{padding:20px 24px;background:linear-gradient(135deg,#0f172a,#1d4ed8);color:#fff}
    h1{margin:0;font-size:24px}
    p{margin:8px 0 0;opacity:.9}
    .grid{display:grid;grid-template-columns:1fr;gap:12px;padding:20px 24px}
    label{font-size:14px;font-weight:700;margin-bottom:6px;display:block}
    input,select,textarea{width:100%;box-sizing:border-box;padding:12px 14px;border:1px solid #cbd5e1;border-radius:12px;font-size:14px}
    textarea{min-height:120px;resize:vertical}
    button{padding:12px 18px;border:0;border-radius:12px;background:#2563eb;color:#fff;font-weight:700;cursor:pointer}
    button:hover{background:#1d4ed8}
    pre{white-space:pre-wrap;background:#0b1220;color:#e5e7eb;padding:20px;margin:0;min-height:200px}
    .row{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
    @media (max-width:700px){.row{grid-template-columns:1fr}}
    .small{font-size:12px;color:#64748b;line-height:1.4}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <header>
        <h1>Серж-ИИ-Кадр</h1>
        <p>Веб-бот для подготовки кадровых документов</p>
      </header>
      <form id="form" class="grid">
        <div class="row">
          <div>
            <label>Тип документа</label>
            <select name="doc_type">
              <option value="Приказ о приёме на работу">Приказ о приёме на работу</option>
              <option value="Приказ о переводе">Приказ о переводе</option>
              <option value="Приказ об увольнении">Приказ об увольнении</option>
              <option value="Справка">Справка</option>
              <option value="Отчёт">Отчёт</option>
              <option value="Штатное расписание">Штатное расписание</option>
            </select>
          </div>
          <div>
            <label>ФИО сотрудника</label>
            <input name="name" placeholder="Иванов Иван Иванович">
          </div>
        </div>
        <div class="row">
          <div>
            <label>Должность</label>
            <input name="position" placeholder="Менеджер по продажам">
          </div>
          <div>
            <label>Дата</label>
            <input name="date" placeholder="21.05.2026">
          </div>
        </div>
        <div>
          <label>Основание / детали</label>
          <textarea name="details" placeholder="Например: заявление работника, трудовой договор, перевод на должность..."></textarea>
        </div>
        <div class="row">
          <button type="submit">Сформировать документ</button>
          <div class="small">Публичная версия работает как прототип. Позже можно подключить ИИ-модель и базу данных.</div>
        </div>
      </form>
      <pre id="out">Готов к работе.</pre>
    </div>
  </div>
  <script>
    const form = document.getElementById('form');
    const out = document.getElementById('out');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      out.textContent = 'Формирование документа...';
      const payload = Object.fromEntries(new FormData(form).entries());
      const r = await fetch('/api/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      const data = await r.json();
      out.textContent = data.text || 'Ошибка генерации';
    });
  </script>
</body>
</html>
"""

@app.get("/")
def index():
    return render_template_string(HTML)

@app.post("/api/generate")
def generate():
    data = request.get_json(force=True) or {}
    doc_type = data.get("doc_type", "Документ")
    name = data.get("name", "")
    position = data.get("position", "")
    date = data.get("date", "")
    details = data.get("details", "")
    text = f"""{doc_type}

Сотрудник: {name}
Должность: {position}
Дата: {date}
Основание: {details}

Проект документа подготовлен в официально-деловом стиле и готов к дальнейшей правке."""
    return jsonify(text=text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
