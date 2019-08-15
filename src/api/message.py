from flask import request, render_template, url_for, redirect, flash, session, Blueprint
from src.DAO.entity import Message, Tag, session_map

message_api = Blueprint('message_api', __name__)


message_statuses = {
    'inreview': 0,
    'aproved': 1,
    'rejected': 2
}


@message_api.route('/send', methods=['POST'])
def send():
    user_id = session.get('user_id')
    title = request.form['title']
    text = request.form['text']
    tag = request.form['tag']

    session_map.add(Message(title, text, tag, user_id))
    session_map.commit()
    return redirect(url_for('message_api.posts'))


@message_api.route('/posts', methods=['GET'])
def posts():
    if 'user_id' in session:
        user_id = session.get('user_id')

        messages = session_map.query(Message).filter_by(status=message_statuses['inreview']).order_by(Message.id.desc())
        messages_reject = session_map.query(Message).filter_by(status=message_statuses['rejected']).order_by(
            Message.id.desc())

        filter_review_admin = session_map.query(Message).filter_by(status=message_statuses['inreview']).all()
        filter_review_user = session_map.query(Message).filter_by(status=message_statuses['inreview'],
                                                                  user_id=user_id).all()

        filter_reject_admin = session_map.query(Message).filter_by(status=message_statuses['rejected']).all()
        filter_reject_user = session_map.query(Message).filter_by(status=message_statuses['rejected'],
                                                                  user_id=user_id).all()

        cnt_filter_review_admin = 0
        for message in filter_review_admin:
            cnt_filter_review_admin += 1

        cnt_filter_review_user = 0
        for message in filter_review_user:
            cnt_filter_review_user += 1

        cnt_filter_reject_admin = 0
        for message in filter_reject_admin:
            cnt_filter_reject_admin += 1

        cnt_filter_reject_user = 0
        for message in filter_reject_user:
            cnt_filter_reject_user += 1

        title = 'Выйти'
        link = '/sign_out'

        return render_template('pages/posts.html',
                               messages=messages,
                               messages_reject=messages_reject,
                               cnt_filter_review_admin=cnt_filter_review_admin,
                               cnt_filter_review_user=cnt_filter_review_user,
                               cnt_filter_reject_admin=cnt_filter_reject_admin,
                               cnt_filter_reject_user=cnt_filter_reject_user,
                               title=title,
                               link=link
                               )

    else:
        return redirect(url_for('login'))


@message_api.route('/post/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    find_message_id = session_map.query(Message).filter_by(id=id).first()
    if find_message_id:
        session_map.delete(find_message_id)
        session_map.commit()
        flash('Сообщение удалено', 'alert-success')
        return redirect(url_for('index'))
    else:
        flash('Не удалось удалить сообщение', 'alert-warning')
        return redirect(url_for('index'))


@message_api.route('/post/reject/<int:id>', methods=['GET', 'POST'])
def reject(id):
    find_message_id = session_map.query(Message).filter_by(id=id).first()

    if find_message_id:
        rejected = message_statuses['rejected']

        find_message_id.status = rejected

        session_map.commit()
        flash('Пост отклонен', 'alert-success')
        return redirect(url_for('message_api.posts'))

    else:
        flash('Пост не отклонен', 'alert-warning')
        return redirect(url_for('message_api.posts'))


@message_api.route('/post/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    title = 'Выйти'
    link = '/sign_out'

    find_message_id = session_map.query(Message).filter_by(id=id).first()
    find_tags = session_map.query(Tag).filter_by(message_id=id).all()

    if request.method == 'POST':
        message_title = request.form['title']
        text = request.form['text']

        find_message_id.title = message_title
        find_message_id.text = text

        session_map.commit()
        return redirect(url_for('message_api.posts'))

    else:
        if find_message_id:
            return render_template('pages/update-post.html',
                                   message=find_message_id,
                                   tag=find_tags,
                                   title=title,
                                   link=link)
        else:
            return redirect(url_for('message_api.posts'))


@message_api.route('/post/confirm/<int:id>', methods=['GET', 'POST'])
def confirm(id):
    if 'user_id' in session:
        find_message_id = session_map.query(Message).filter_by(id=id).first()

        if find_message_id:
            find_message_id.status = 1
            session_map.commit()
            flash('Пост подтвержден', 'alert-success')
            return redirect(url_for('message_api.posts'))
        else:
            flash('Пост не подтвержден', 'alert-warning')
            return redirect(url_for('index'))