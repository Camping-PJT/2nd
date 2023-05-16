// const postItems = document.querySelectorAll('.post-item');

// postItems.forEach((postItem) => {
//   postItem.addEventListener('dragstart', (event) => {
//     event.dataTransfer.setData('text/plain', event.target.dataset.postId);
//   });
// });

// const priorityDropzones = document.querySelectorAll('.priority-dropzone');
// const postList = document.querySelector('.post-list');

// priorityDropzones.forEach((dropzone) => {
//   const priority = parseInt(dropzone.dataset.priority);

//   dropzone.addEventListener('dragover', (event) => {
//     event.preventDefault();
//   });

//   dropzone.addEventListener('dragenter', (event) => {
//     event.preventDefault();
//     event.currentTarget.classList.add('highlight');
//   });

//   dropzone.addEventListener('dragleave', (event) => {
//     event.currentTarget.classList.remove('highlight');
//   });

//   dropzone.addEventListener('drop', (event) => {
//     event.preventDefault();
//     event.currentTarget.classList.remove('highlight');

//     const postId = event.dataTransfer.getData('text/plain');
//     const priority = event.currentTarget.dataset.priority;
//     const postTitle = document.querySelector(`.post-item[data-post-id="${postId}"] label`).textContent;
    
//     const inputElement = document.createElement('input');
//     inputElement.type = 'hidden';
//     inputElement.name = 'priority_updates[]';
//     inputElement.value = `${postId}:${priority}`;

//     document.getElementById('priority-form').appendChild(inputElement);

//     const postItem = document.querySelector(`.post-item[data-post-id="${postId}"]`);
//     postItem.style.display = 'none';

//     event.currentTarget.textContent = postTitle;


//     document.getElementById('priority-form').submit();
//   });
// });
// 위까지는 ajax x



// window.addEventListener('DOMContentLoaded', () => {
//   const postItems = document.querySelectorAll('.post-item');
//   const priorityDropzones = document.querySelectorAll('.priority-dropzone');

//   postItems.forEach((postItem) => {
//     postItem.addEventListener('dragstart', (event) => {
//       event.dataTransfer.setData('text/plain', event.target.dataset.postId);
//     });
//   });

//   priorityDropzones.forEach((dropzone) => {
//     const priority = parseInt(dropzone.dataset.priority);

//     dropzone.addEventListener('dragover', (event) => {
//       event.preventDefault();
//     });

//     dropzone.addEventListener('dragenter', (event) => {
//       event.preventDefault();
//       event.currentTarget.classList.add('highlight');
//     });

//     dropzone.addEventListener('dragleave', (event) => {
//       event.currentTarget.classList.remove('highlight');
//     });

//     dropzone.addEventListener('drop', (event) => {
//       event.preventDefault();
//       event.currentTarget.classList.remove('highlight');

//       const postId = event.dataTransfer.getData('text/plain');
//       const priority = event.currentTarget.dataset.priority;
//       const postTitle = document.querySelector(`.post-item[data-post-id="${postId}"] label`).textContent;

//       const inputElement = document.createElement('input');
//       inputElement.type = 'hidden';
//       inputElement.name = 'priority_updates[]';
//       inputElement.value = `${postId}:${priority}`;

//       document.getElementById('priority-form').appendChild(inputElement);

//       const postItem = document.querySelector(`.post-item[data-post-id="${postId}"]`);
//       postItem.style.display = 'none';

//       event.currentTarget.textContent = postTitle;

//       const form = document.getElementById('priority-form');
//       const formData = new FormData(form);

//       fetch(form.action, {
//         method: form.method,
//         body: formData,
//       })
//         .then((response) => {
//           if (response.ok) {
//             // 성공
//           } else {
//             throw new Error('Priority update failed');
//           }
//         })
//         .catch((error) => {
//           console.error(error);
//         });
//     });
//   });
// });

window.addEventListener('DOMContentLoaded', () => {
  const postItems = document.querySelectorAll('.post-item');
  const priorityDropzones = document.querySelectorAll('.priority-dropzone');

  postItems.forEach((postItem) => {
    postItem.addEventListener('dragstart', (event) => {
      event.dataTransfer.setData('text/plain', event.target.dataset.postId);
    });
  });

  priorityDropzones.forEach((dropzone) => {
    const priority = parseInt(dropzone.dataset.priority);

    dropzone.addEventListener('dragover', (event) => {
      event.preventDefault();
    });

    dropzone.addEventListener('dragenter', (event) => {
      event.preventDefault();
      event.currentTarget.classList.add('highlight');
    });

    dropzone.addEventListener('dragleave', (event) => {
      event.currentTarget.classList.remove('highlight');
    });

    dropzone.addEventListener('drop', (event) => {
      event.preventDefault();
      event.currentTarget.classList.remove('highlight');

      const postId = event.dataTransfer.getData('text/plain');
      const priority = event.currentTarget.dataset.priority;
      const postTitle = document.querySelector(`.post-item[data-post-id="${postId}"] label`).textContent;

      const inputElement = document.createElement('input');
      inputElement.type = 'hidden';
      inputElement.name = 'priority_updates[]';
      inputElement.value = `${postId}:${priority}`;

      document.getElementById('priority-form').appendChild(inputElement);

      const postItem = document.querySelector(`.post-item[data-post-id="${postId}"]`);
      postItem.style.display = 'none';

      event.currentTarget.textContent = postTitle;

      const form = document.getElementById('priority-form');
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
      const formData = new FormData(form);

      axios({
        method: form.method,
        url: form.action,
        data: formData,
        headers: {'X-CSRFToken': csrftoken},
      })
        .then((response) => {
          if (response.status === 200) {
            // Success
          } else {
            throw new Error('Priority update failed');
          }
        })
        .catch((error) => {
          console.error(error);
        });
    });
  });
});
