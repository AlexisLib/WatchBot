<?php 
	require 'db_info.php';
	
	$mail = mysqli_real_escape_string($conn, $_POST['mail']);
	$password = mysqli_real_escape_string($conn, $_POST['password']);
	
	if(empty($mail) || empty($password)){
		header("Location: ../signin.php");
		exit();	
	}
	else {
			$sql = "SELECT * FROM user WHERE mail=?;";
			$stmt = mysqli_stmt_init($conn);
			if(!mysqli_stmt_prepare($stmt, $sql)){
				echo "SQL : Get user failed";
			}
			else {
				mysqli_stmt_bind_param($stmt, "s", $mail);
				mysqli_stmt_execute($stmt);
				$result = mysqli_stmt_get_result($stmt);
				if($row = mysqli_fetch_assoc($result)){
					$pwdCheck = password_verify($password, $row['password']);
					if($pwdCheck == false){
						header("location: ../signin.php?error=wrongpwd");
						exit();
					}
					else{
						session_start();
						$_SESSION["iduser"] = $row['id'];
						$_SESSION["gender"] = $row['gender'];
						$_SESSION["firstname"] = $row['firstname'];
						$_SESSION["lastname"] = $row['lastname'];
						$_SESSION["age"] = $row['age'];
						$_SESSION["height"] = $row['height'];
						$_SESSION["weight"] = $row['weight'];
						$_SESSION["idwatch"] = $row['idwatch'];
						$_SESSION["modelwatch"] = $row['modelwatch'];
						header("location: ..");
						exit();
					}
				}
				else{
					header("location: ../signin.php?error=wrongmail");
					exit();
				}
			}
		}
		mysqli_stmt_close($stmt);
		mysqli_close($conn);
		header("location: ../signin.php");
		exit();
?>