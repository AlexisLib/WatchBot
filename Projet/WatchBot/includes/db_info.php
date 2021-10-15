<?php
#include_once 'includes/db_info.php';
$dbServername = "localhost";
$dbUsername = "root";
$dbPassword = "";
$dbName = "watchbot";

$conn = mysqli_connect($dbServername, $dbUsername, $dbPassword, $dbName);

$conn->set_charset("utf8");

if(!$conn) {
	die("Connection failed: ".mysqli_connect_error());
}
?>