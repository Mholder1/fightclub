<?php

echo("inside php");



$dbServername = "localhost";
$dbPort = "5432"
$dbUsername = "postgres";
$dbName = "postgres";
$dbPassword = "root";

$connect = mysql_connect($dbServername, $dbPort, $dbUsername, $dbName, $dbPassword);



$person = $_POST['person'];
$email = $_POST['email'];

$sql = "INSERT INTO list_fighters ('person', 'email') 
VALUES ($person, $email);";
mysqli_query($connect, $sql);

header("Location: ../index.html?signup=success)";

?>
