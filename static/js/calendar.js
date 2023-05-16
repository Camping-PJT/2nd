document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    locale: 'ko',
    droppable: true,
    editable: true,
    businessHours: true,
    dayMaxEvents: true,
    events: function(info, successCallback, failureCallback) {
      // AJAX 요청을 통해 서버에서 데이터를 가져옴
      $.ajax({
        url: '/schedules/get_schedule_data/',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
          // 가져온 데이터를 이벤트 목록에 추가
          var events = response.map(function(schedule) {
            return {
              title: schedule.title,
              start: schedule.start,
              end: schedule.end,
              url: schedule.url, // 스케줄 변경 URL 설정
              extendedProps: {
                post_id: schedule.post_id,
                description: schedule.description,
                schedule_id: schedule.schedule_id // 스케줄 ID 추가
              }
            };
          });
          successCallback(events);
        },
        error: function(xhr, status, error) {
          failureCallback(xhr, status, error);
        }
      });
    },
    eventClick: function(info) {
      // 상세 페이지로 바로 이동
      window.location.href = info.event.url.replace('update', 'detail');
    
      // 기본 이벤트 동작 취소
      info.jsEvent.preventDefault();
    }
  });
  calendar.render();
});