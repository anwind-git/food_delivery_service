$(document).ready(function() {
            setInterval(function() {
                updateOrderData();
            }, 30000);

            function updateOrderData() {
                $.ajax({
                    url: window.location.href,
                    type: 'GET',
                    success: function(data) {
                        $('#order-container').html($(data).find('#order-container').html());
                    },
                    error: function(error) {
                        console.error('Error updating order data:', error);
                    }
                });
            }
        });