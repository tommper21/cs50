document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-view').onsubmit = function() {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify ({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
    });
    load_mailbox('sent');
    //prevent default submission
    return false;
  }

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#mail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

      // display all email elements
      emails.forEach(email => {
        const element = document.createElement('div');
        element.className = 'element';
        element.innerHTML = `<b>${email.sender}</b> ${email.subject} <i style="float:right">${email.timestamp}</i>`;
        if (email.read) {
          element.style.background = 'lightgray';
        }

        // mark as read and display the mail view when clicked on
        element.addEventListener('click', function() {
          element.style.background = 'lightgray';
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
              read: true
            })
          })
          let un_archive = 'Unarchive';
          if (`${mailbox}` == 'inbox') {
            un_archive = 'Archive';
          }

            document.querySelector('#mail-view').innerHTML =
            `<p> <b>From:</b> ${email.sender}</p>
             <p> <b>To:</b> ${email.recipients}</p>
             <p> <b>Subject:</b> ${email.subject}</p>
             <p> <b>Timestamp:</b> ${email.timestamp}</p>
             <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
             <button class="btn btn-sm btn-outline-primary" id="archive">${un_archive}</button>
             <hr>
             <p> ${email.body}</p>`;
             if (`${mailbox}` == 'sent') {
               document.querySelector('#archive').style.display = 'none';
             }
            document.querySelector('#emails-view').style.display = 'none';
            document.querySelector('#mail-view').style.display = 'block';
            document.querySelector('#archive').addEventListener('click', function() {
              // check if already Archived
              let bool = true;
              if (email.archived == true) {
                bool = false;
              }

              fetch(`/emails/${email.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                  archived: bool
                })
              })
              load_mailbox('inbox');
            })
            document.querySelector('#reply').addEventListener('click', function () {
              document.querySelector('#emails-view').style.display = 'none';
              document.querySelector('#mail-view').style.display = 'none';
              document.querySelector('#compose-view').style.display = 'block';

              // Clear out composition fields
              document.querySelector('#compose-recipients').value = `${email.sender}`;
              if (`${email.subject}`.startsWith('Re:')) {
                document.querySelector('#compose-subject').value = `${email.subject}`;
              }
              else {
                document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
              }

              document.querySelector('#compose-body').value =`On ${email.timestamp} ${email.sender} wrote: ${email.subject}`;

            })



        });
        document.querySelector('#emails-view').append(element);
      })
    });
}
