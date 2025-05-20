from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
import markdown
import json
import os

class QuizPlugin(BasePlugin):
    config_scheme = (
        ('quiz_dir', config_options.Type(str, default='quizzes')),
    )

    def on_page_markdown(self, markdown_content, page, config, files):
        quiz_marker = "[[quiz:"
        new_lines = []
        for line in markdown_content.split('\n'):
            if line.strip().startswith(quiz_marker):
                filename = line.strip()[len(quiz_marker):-2].strip()
                full_path = os.path.join(self.config['quiz_dir'], filename)
                with open(full_path, 'r', encoding='utf-8') as f:
                    quiz_data = json.load(f)
                html = self.generate_quiz_html(quiz_data)
                new_lines.append(html)
            else:
                new_lines.append(line)
        return '\n'.join(new_lines)

    def on_post_page(self, output_content, page, config):
        # Inject JS for quiz logic
        script = """
<script>
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".quiz-form").forEach(form => {
        form.addEventListener("submit", e => {
            e.preventDefault();
            const formData = new FormData(form);
            const answers = {};
            formData.forEach((value, key) => {
                if (!answers[key]) answers[key] = [];
                answers[key].push(value);
            });
            const results = JSON.parse(form.dataset.answers);
            form.querySelectorAll(".feedback").forEach(el => el.remove());
            for (let qid in results) {
                const correct = results[qid];
                const given = answers[qid] || [];
                const feedback = document.createElement("div");
                feedback.className = "feedback";
                feedback.style.marginTop = "5px";
                if (JSON.stringify(correct.sort()) === JSON.stringify(given.sort())) {
                    feedback.innerHTML = "<b style='color: green;'>✔ Correct!</b>";
                } else {
                    feedback.innerHTML = "<b style='color: red;'>✘ Incorrect.</b> Correct answer: " + correct.join(", ");
                }
                form.querySelector(`#${qid}`).appendChild(feedback);
            }
        });
    });
});
</script>
"""
        return output_content + script

    def generate_quiz_html(self, quiz_data):
        html = ['<form class="quiz-form" data-answers=\'{}\'><div>'.format(json.dumps({
            q['id']: q['answer'] if isinstance(q['answer'], list) else [q['answer']]
            for q in quiz_data['questions']
        }))]
        for q in quiz_data['questions']:
            html.append(f"<div id='{q['id']}'><p><strong>{q['question']}</strong></p>")
            qtype = q.get('type', 'single')
            if qtype == 'open':
                html.append(f"<textarea name='{q['id']}' rows='3' cols='40'></textarea>")
            else:
                for opt in q['options']:
                    input_type = 'checkbox' if qtype == 'multiple' else 'radio'
                    html.append(f"<label><input type='{input_type}' name='{q['id']}' value='{opt}'> {opt}</label><br>")
            html.append("</div><br>")
        html.append('<button type="submit">Submit Answers</button></div></form>')
        return '\n'.join(html)
