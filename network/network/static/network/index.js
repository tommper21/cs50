document.addEventListener('DOMContentLoaded', function() {

  document.querySelectorAll('.edit-button').forEach(button => {
    button.addEventListener('click', function() {
    let div = button.parentElement;
    const text = div.getElementsByTagName('P')[0].innerHTML;
    div.innerHTML =
    `
    <div class="form-group">
        <textarea class="form-control">${text}</textarea>
    </div>
    <button class="btn btn-primary btn-sm save-button">Save</button>`;

    });
  });

  document.addEventListener('click', event => {
    const element = event.target;
    if (element.className === 'btn btn-primary btn-sm save-button') {
      let div = element.parentElement;
      const text = div.getElementsByTagName('TEXTAREA')[0].value;
      div.innerHTML =
      `<button class="btn btn-outline-primary btn-sm edit-btn">Edit</button>
      <p>${text}</p>`;

      // sende neuen body via JSON
      fetch(`/posts/${div.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          body: text
        })
      })

      const button = document.querySelector('.edit-btn')
      if (button) {
        button.addEventListener('click', function() {
        let div = button.parentElement;
        const text = div.getElementsByTagName('P')[0].innerHTML;
        div.innerHTML =
        `
        <div class="form-group">
            <textarea class="form-control">${text}</textarea>
        </div>
        <button class="btn btn-primary btn-sm save-button">Save</button>`;

        });
      }
    }
  })
  document.addEventListener('click', event => {
    const element = event.target;
    if (element.className == 'like-button') {

      fetch(`/likes/${element.name}`)
      .then(response => response.json())
      .then(post => {
        console.log(post.likes);
        // now update the likes
        const div = element.parentElement;
        div.getElementsByTagName('SPAN')[0].innerHTML = post.likes;
      })
    }
  })
})
