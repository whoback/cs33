document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  // submit button for sending emails
  document.querySelector('#compose-form').addEventListener('submit', send_email);
  // By default, load the inbox
  load_mailbox('inbox');
});

// inspired by Hints section @ https://cs50.harvard.edu/extension/web/2021/spring/projects/3/mail/
function make_el(el, content, css = null) {
  const c = document.createElement(el);
  c.innerHTML = content;
  if (css !== null) {
    css.split(' ').forEach(css => {
      c.classList.add(css);
    });
  }
  return c;
}
// only show the view we want
function switch_view(selector) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-view').style.display = 'none';

  document.querySelector(selector).style.display = 'block';
}

function compose_email() {

  switch_view('#compose-view')
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

// grab an email and mark it as read
function mark_as_read(email_id) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
    .then(res => {
      if (res.ok !== true) {
        console.log(`Error: ${res}`);
      }
    });
}

// grab an eamil and change its archive status
function set_archive(msg) {
  fetch(`/emails/${msg.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !msg.archived
    })
  })
    .then(res => {
      if (res.ok == true) {
        switch_view('inbox');
      } else {
        console.log(`Error: ${res}`);
      }
    })
}

var globalMailbox;

// load the selected mailbox
function load_mailbox(mailbox) {
  globalMailbox = mailbox;

  const msg_list = document.createElement('div');

  // grab emails
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

      msg_list.innerHTML = '';
      const num_of_emails = emails.length;
      msg_list.appendChild(make_el('p', `${num_of_emails} message${(num_of_emails === 1 ? '' : 's')}`));

      if (num_of_emails > 0) {
        for (const email in emails) {
          const email_entry = make_el('div', null, 'btn-outline-primary clickable');
          email_entry.addEventListener('click', () => get_email(emails[email].id));
          if (emails[email].read === true) {
            email_entry.classList.add('read');
          }
          if (mailbox === 'sent') {
            email_entry.appendChild(make_el('span', `To:  ${emails[email].recipients}`, 'message-address'));
          } else {
            email_entry.appendChild(make_el('span', `From:  ${emails[email].sender}`, 'message-address'));
          }
          email_entry.appendChild(make_el('span', `&emsp;${emails[email].subject}`));
          email_entry.appendChild(make_el('span', `&emsp;${emails[email].timestamp}`, 'last'));

          msg_list.appendChild(email_entry);

        }
      }

    })

  // Show the mailbox and hide other views
  switch_view('#emails-view');

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  document.querySelector('#emails-view').appendChild(msg_list);
}


// grab form data and send using JS
function send_email() {
  event.preventDefault();

  // grab data
  form = document.querySelector('#compose-form');
  to = form.querySelector('#compose-recipients').value;
  subject = form.querySelector('#compose-subject').value;
  body = form.querySelector('#compose-body').value;

  // do work
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: to,
      subject: subject,
      body: body
    })
  })
    .then(response => response.json())
    .then(result => {
      // load mailbox or error
      error = result.error;
      if (error !== undefined) {
        alert(error);
      } else {
        load_mailbox('sent');
      }
    });


}

function send_reply(msg) {
  compose_email(); //load form and autopop fields
  document.querySelector('#compose-recipients').value = msg.sender;
  if (msg.subject.slice(0, 4) == 'Re: ') {
    document.querySelector('#compose-subject').value = msg.subject;
  } else {
    document.querySelector('#compose-subject').value = `Re: ${msg.subject}`;
  }
  document.querySelector('#compose-body').value = `\n\n\nOn ${msg.timestamp} ${msg.sender} wrote:\n\n${msg.body}`;
}

function get_email(email_id) {
  //grab single email and style it
  fetch(`/emails/${email_id}`)
    .then(res => res.json())
    .then(email => {
      mark_as_read(email_id);

      const content_div = document.createElement('div');
      const btns_div = make_el('div', '', 'action-buttons');

      if (globalMailbox !== 'sent') {
        const archive_btn = make_el('button', '', 'mailbox-button btn btn-primary');
        if (email.archived == true) {
          archive_btn.innerHTML = 'Unarchive';
        } else {
          archive_btn.innerHTML = 'Archive';
        }
        archive_btn.addEventListener('click', () => set_archive(email));
        btns_div.appendChild(archive_btn);
      }

      const reply_btn = make_el('button', 'Reply', 'mailbox-button btn btn-primary');
      reply_btn.addEventListener('click', () => send_reply(email));
      btns_div.appendChild(reply_btn);

      content_div.appendChild(btns_div);
      content_div.appendChild(make_el('h4', `From:  ${email.sender}`));
      content_div.appendChild(make_el('h4', `To:  ${email.recipients}`));
      content_div.appendChild(make_el('h4', `Subject:  ${email.subject}`));
      content_div.appendChild(make_el('h4', email.timestamp));

      let msg_body = '';
      email.body.split('\n').forEach(line => {
        msg_body += `${line}<br>`;
      });
      content_div.appendChild(make_el('p', msg_body, 'body'));

      document.querySelector('#single-view').innerHTML = '';
      document.querySelector('#single-view').appendChild(content_div);
    });

  switch_view('#single-view');
}