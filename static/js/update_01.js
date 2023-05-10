function confirmDelete(event) {
  event.preventDefault()

  if (confirm("정말로 탈퇴하시겠습니까?")) {
    document.querySelector("#delete").submit()
  }
}