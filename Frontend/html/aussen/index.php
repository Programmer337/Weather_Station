<?php
error_reporting(E_ALL);
header ("Expires: Mon, 26 Jul 1997 05:00:00 GMT"); // Datum der Vergangenheit
header ("Last-Modified: " . gmdate ("D, d M Y H:i:s") . " GMT"); // immer geändert
header ("Cache-Control: no-cache, must-revalidate"); // HTTP/1.1
header ("Pragma: no-cache");
date_default_timezone_set('Europe/Berlin');

$valid_last = ['last24', 'week', 'month','year'];
$valid_period = ['day', 'month', 'year'];
if (isset($_POST['last']) && in_array($_POST['last'], $valid_last, TRUE)){
    $last = $_POST['last'];

    standard:
    $edit = date("Y-m-d H:i:s", filemtime("pictures/" . $last . ".svg"));
    if($edit < date("Y-m-d H:00:00")){
        shell_exec("python3 ../../plot.py " . $last);
    }
    $image = '<img src="pictures/' . $last . '.svg">';
}
else if(isset($_POST['period']) && in_array($_POST['period'], $valid_period)){
    $period = $_POST['period'];
    $date = $_POST['date'];
    if (!strtotime($date)){
        $image = "Diese Eingabe ist keine gültige Zeitangabe. Hast  du alles ausgefüllt?";
    }
    else{
        $len = strlen($date);
        if($len == 4 && $period=="year" or $len == 7 && $period =="month" or $len==10&& $period=="day"){
            $invalid = FALSE;
            switch ($period){
                case 'day':
                    if($date >= date("Y-m-d")){
                        $invalid = TRUE;
                    }
                    break;
                case 'month':
                    if($date >= date("Y-m")){
                        $invalid = TRUE;
                    }
                    break;
                case 'year':
                    if($date >= date("Y")){
                        $invalid = TRUE;
                    }
                    break;
            }
            if($invalid){
                $image = "Bitte gib eine Vergangene Zeit an";
            }
            else{
                if(!file_exists("pictures/" . $date . ".svg")){
                    shell_exec("python3 ../../plot.py " . $period . " " .$date);
                }
                $image = '<img src="pictures/' . $date . '.svg">';
            }
        }
    }
}
else{
    $last = "last24";
    goto standard;
}
?>

<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="/style.css">
    <script src="/script.js"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wetterstation aussen</title>
</head>
<body>
    <noscript>Javascript konnte nicht geladen werden</noscript>
    <div class="center">
        <?php
        echo $image;
        ?>
    </div>
    <div class="center-desktop">
        <div class="center">
            <h2>Verlauf ansehen: </h2>
        </div>
        <div class="center">
            <form method="post">
                <select name="last" id="last">
                    <option value="last24">24 Stunden</option>
                    <option value="week">Diese Woche</option>
                    <option value="year">Dieses Jahr</option>
                    <option value="month">Diesen Monat</option>
                </select>
                <button>Anzeigen</button>
            </form>
        </div>
    </div>
    <div class="center-desktop">
        <div class="center">
            <h2>Bestimmter Zeitraum: </h2>
        </div>
        <div class="center">
            <form method="post">
                <select name="period" id="period">
                    <option value="day">Tag</option>
                    <option value="month">Monat</option>
                    <option value="year">Jahr</option>
                </select>
                <input type="date" name="date" id="date">
                <button>Anzeigen</button>
            </form>
        </div>
    </div>
    <div class="center">
        <a href="/innen">Wetterstation innen</a>
    </div>
</body>
</html>