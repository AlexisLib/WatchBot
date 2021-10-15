<?php 
	require 'db_info.php';
	
	$gender = mysqli_real_escape_string($conn, $_POST['gender']);
	$firstname = mysqli_real_escape_string($conn, $_POST['firstname']);
	$lastname = mysqli_real_escape_string($conn, $_POST['lastname']);
	$age = mysqli_real_escape_string($conn, $_POST['age']);
	$height = mysqli_real_escape_string($conn, $_POST['height']);
	$weight = mysqli_real_escape_string($conn, $_POST['weight']);
	$mail = mysqli_real_escape_string($conn, $_POST['mail']);
	$password = mysqli_real_escape_string($conn, $_POST['password']);
	$idwatch = mysqli_real_escape_string($conn, $_POST['idwatch']);
	$modelwatch = mysqli_real_escape_string($conn, $_POST['modelwatch']);
	
	if(empty($gender) || empty($firstname) || empty($lastname) || empty($age) || empty($height) || empty($weight) || empty($mail) || empty($password) || empty($idwatch) || empty($modelwatch)){
		header("Location: ../signup.php");
		exit();	
	}
	
	$hashedpassword = password_hash($password, PASSWORD_DEFAULT);
	$sql = "INSERT INTO user (id, gender, firstname, lastname, age, height, weight, mail, password, idwatch, modelwatch) VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);";
	$stmt = mysqli_stmt_init($conn);
	if(!mysqli_stmt_prepare($stmt, $sql)){
		echo "SQL error add user";
	}
	else{
		mysqli_stmt_bind_param($stmt, "sssiiissis", $gender, $firstname, $lastname, $age, $height, $weight, $mail, $hashedpassword, $idwatch, $modelwatch);
		mysqli_stmt_execute($stmt);
		
		$memory = fopen('../python/memory'.$idwatch.'.json', 'w');
		fwrite($memory, '{"type": "", "nb_reponse": 0, "type_demande": "", "periode": ""}');
		fclose($memory);
		
		header("Location: ../signin.php");
		exit();
	}
?>