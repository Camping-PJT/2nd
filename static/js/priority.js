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

//

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
//       const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
//       const formData = new FormData(form);

//       axios({
//         method: form.method,
//         url: form.action,
//         data: formData,
//         headers: {'X-CSRFToken': csrftoken},
//       })
//         .then((response) => {
//           if (response.status === 200) {
//             // Success
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

(() => {
  axios.defaults.xsrfCookieName = 'csrftoken';
  axios.defaults.xsrfHeaderName = 'X-CSRFToken';
  const $ = (select) => document.querySelectorAll(select);
  const draggables = $('.draggable');
  const containers = $('.box4--left');

  draggables.forEach(el => {
    el.addEventListener('dragstart', () => {
        el.classList.add('dragging');
    });

    el.addEventListener('dragend', () => {
        el.classList.remove('dragging');
        // 드랍 이벤트 발생 후 좋아요 리스트와 우선순위 리스트 업데이트
        updateLists();
    });
  });

  function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.draggable:not(.dragging)')];

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
          return { offset: offset, element: child };
        } else {
          return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
  }

  function updateLists() {
    const likedPosts = [];
    const priorityPosts = [];

     // 좋아요 리스트 업데이트
    const likedContainer = document.getElementById('postdrop');
    likedContainer.querySelectorAll('.draggable').forEach(el => {
        likedPosts.push(parseInt(el.getAttribute('data-post-id')));
    });
    console.log(likedPosts)

     // 우선순위 리스트 업데이트
    const priorityContainer = document.getElementById('prioritydrop');
    priorityContainer.querySelectorAll('.draggable').forEach((el, index) => {
        const postId = parseInt(el.getAttribute('data-post-id'));
        const priority = index + 1;
        priorityPosts.push({ postId, priority });
        console.log({ postId, priority })
    });
    console.log(priorityPosts)

     // 좋아요 리스트와 우선순위 리스트를 서버로 전송하여 저장
    const userId = document.getElementById('user_id').value;
    console.log(userId)
    saveListsToServer(userId, likedPosts, priorityPosts);
  }

  function saveListsToServer(userId, likedPosts, priorityPosts) {
    // 좋아요 리스트와 우선순위 리스트를 서버로 전송하여 저장
    const url = '/posts/update_priority_lists/';
    console.log(userId, likedPosts, priorityPosts)
    axios.post(url, {
      userId: userId, 
      likedPosts: likedPosts,
      priorityPosts: priorityPosts,
    },{
    headers: {
      'Content-Type': 'application/json'}
    })
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.log('안넘어감');
      });
  }

  containers.forEach(container => {
    container.addEventListener('dragover', e => {
    e.preventDefault();
    const afterElement = getDragAfterElement(container, e.clientY);
    const draggable = document.querySelector('.dragging');
    container.insertBefore(draggable, afterElement);
    });
  });
})
();