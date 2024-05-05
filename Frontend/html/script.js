document.addEventListener("DOMContentLoaded", function (){
    let period = document.getElementById("period");
    period.addEventListener("change", change);

    function change(){
        let date = document.getElementById("date");
        switch(period.value){
            case('day'): 
                date.type = "date";
                break;
            case('month'): 
                date.type = "month";
                break;
            case('year'): 
                date.type = "number";
                break;
            default:
                date.type = "date";
        }
    }
});