<?php session_start(); ?>
<?php include_once 'db_info.php'; ?>

<?php
	$sql = "DELETE FROM chat WHERE iduser=?;";
	$stmt = mysqli_stmt_init($conn);
	if(!mysqli_stmt_prepare($stmt, $sql)){
		echo "SQL : Get playlist failed";
	}
	else {
		mysqli_stmt_bind_param($stmt, "i", $_SESSION["iduser"]);
		mysqli_stmt_execute($stmt);
	}
	
	$path = getcwd();
	$path = dirname($path);
	$path = $path."\python";
	chdir($path);
	
	$iduser = $_SESSION["iduser"];
	
	$command = escapeshellcmd("ClearMemory.py " .$iduser);
	$output = shell_exec($command);
	echo $output;
	
	header("Location: ..");
	exit();
?>