from flask import Flask, render_template
import random

app = Flask(__name__)

phrases = [
            {'phrase': 'Дойдя до конца, люди смеются над страхами, мучившими их вначале.', 'author': 'Пауло Коэльо'},
            {'phrase': 'Если ты не знаешь, чего хочешь, ты в итоге останешься с тем, чего точно не хочешь.',
             'author': 'Чак Паланик'},
            {'phrase': 'Чтобы дойти до цели, надо идти.', 'author': 'Оноре де Бальзак'},
            {'phrase': 'Это своего рода забава, делать невозможное.', 'author': 'Уолт Дисней'},
            {'phrase': 'К черту все! Берись и делай!', 'author': 'Ричард Брэнсон'},
            {'phrase': 'Пробуйте и терпите неудачу, но не прерывайте ваших стараний.', 'author': 'Стивен Каггва'}]


def generate_phrase():
    generated_phrase = random.choice(phrases)

    return generated_phrase


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', phrase=generate_phrase(), posts=phrases)


@app.route('/contact')
def contact():
    return render_template('contact.html', phrase=generate_phrase(), posts=phrases)


if __name__ == '__main__':
    app.run(debug=False)
