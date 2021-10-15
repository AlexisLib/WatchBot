<!DOCTYPE html>
<html style="background-color: #555555;">

	<head>
		<title>WatchBot</title>
		<!--Logo-->
        <link rel="icon" type="images/png" href="images/bot.png">
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
		<link rel="stylesheet" href="css/theme.css"/>
	</head>
	
	<body style="background-color:rgba(0, 0, 0, 0.0);">
	
		<nav class="navbar navbar-expand-sm bg-dark navbar-dark fixed-top">
			<ul class="navbar-nav">
				<li class="nav-item">
					<a class="navbar-brand" href="index.php">Watchbot</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="index.php">Home</a>
				</li>
			</ul>
			<div class="navbar-collapse collapse w-100 order-3 dual-collapse2">
				<ul class="navbar-nav ml-auto">
					<li class="nav-item">
						<a class="nav-link" href="signin.php">Sign In</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="signup.php">Sign Up</a>
					</li>
				</ul>
			</div>
		</nav>
	
		<div style="display:flex;justify-content:center;align-items:center;height:100vh;">
			<div class="card signupcard">
				<div class="card-body">
					<img class="mx-auto d-block" src="images/bot.png" width="30%">
					<br>
					<h4 class="card-title text-white text-center">Create your account</h4>
					<br>
					<form id="formadduser" autocomplete="off" action="includes/adduser.php" method="POST">
						<div class="form-group">
							<label class="text-white">Gender :</label>
							<div class="row">
								<div class="col-sm-6">
									<div class="form-check">
										<input class="form-check-input" type="radio" name="gender" id="male" value="male" checked>
										<label class="form-check-label text-white" for="male">Male</label>
									</div>
								</div>       
							   <div class="col-sm-6">
									<div class="form-check">
										<input class="form-check-input" type="radio" name="gender" id="female" value="female">
										<label class="form-check-label text-white" for="female">Female</label>
									</div>
							   </div> 
							</div>
						</div>
						<div class="form-group">
							<div class="row">
							   <div class="col-sm-6">
								 <label for="firstname" class="text-white">First name :</label>
								 <input id="firstname" class="form-control input-group-lg reg_name" type="text" name="firstname" placeholder="First name" required>
							   </div>       
							   <div class="col-sm-6">
								 <label for="lastname" class="text-white">Last name :</label>
								 <input id="lastname" class="form-control input-group-lg reg_name" type="text" name="lastname" placeholder="Last name" required>
							   </div>
							 </div>
						</div>
						<div class="form-group">
							<div class="row">
							   <div class="col-sm-4">
								 <label for="age" class="text-white">Age :</label>
								 <input id="age" class="form-control input-group-lg reg_name" type="text" name="age" placeholder="Age" required>
							   </div>       
							   <div class="col-sm-4">
								 <label for="height" class="text-white">Height :</label>
								 <input id="height" class="form-control input-group-lg reg_name" type="text" name="height" placeholder="Height (Cm)" required>
							   </div>
							   <div class="col-sm-4">
								 <label for="weight" class="text-white">Weight :</label>
								 <input id="weight" class="form-control input-group-lg reg_name" type="text" name="weight" placeholder="Weight (Kg)" required>
							   </div>
							 </div>
						</div>
						<div class="form-group">
							<label class="text-white" for="mail">Mail :</label>
							<input type="text" class="form-control" name="mail" placeholder="Mail" id="mail" required>
						</div>
						<div class="form-group">
							<div class="row">
								<label class="col text-white" for="password">Password :</label>
								<label class="col checkbox text-white text-right"><input type="checkbox" onclick="showpassword();"> Show</label>
							</div>
							<input type="password" class="form-control" name="password" placeholder="Password" id="password" required>
						</div>
						<div class="form-group">
							<div class="row">
							   <div class="col-sm-6">
								 <label for="idwatch" class="text-white">ID of your watch :</label>
								 <input id="idwatch" class="form-control input-group-lg" type="text" name="idwatch" placeholder="ID" required>
							   </div>       
							   <div class="col-sm-6">
									<label class="text-white" for="model">Model of your watch :</label>
									<select class="form-control" name="modelwatch" id="model" required>
										<option>WatchBot Serie 1</option>
									</select>
							   </div>
							 </div>
						</div>
					</form>
					<br>
					<div class="text-center">
						<button name="adduser" type="submit" form="formadduser" class="btn btn-primary" style="width:200px;">Create your account</button>
					</div>
					<br>
				</div>
			</div>
		</div>
	
	</body>
	
	<script>
		//Show password
        function showpassword(){
            var inputpassword = document.getElementById("password");
            if (inputpassword.type === "password") {
                inputpassword.type = "text";
            } 
            else {
                inputpassword.type = "password";
            }
        }
	</script>
	
</html>