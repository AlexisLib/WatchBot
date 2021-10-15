<?php session_start(); ?>
<?php include_once 'includes/db_info.php'; ?>

<!DOCTYPE html>
<html>

	<head>
		<title>WatchBot</title>
		<!--Logo-->
        <link rel="icon" type="images/png" href="images/bot.png">
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.2/css/all.min.css"/>
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
		<link rel="stylesheet" href="css/theme.css"/>
		<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/malihu-custom-scrollbar-plugin/3.1.5/jquery.mCustomScrollbar.min.css">
		<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/malihu-custom-scrollbar-plugin/3.1.5/jquery.mCustomScrollbar.min.js"></script>
	</head>
	
	<style>
		/*Eliminates padding, centers the thumbnail */

		body, html {
		padding: 0;
		margin: 0;
		text-align: center;
		}

		/* Styles the thumbnail */

		a.lightbox img {
		height: 150px;
		border: 3px solid white;
		box-shadow: 0px 0px 8px rgba(0,0,0,.3);
		margin: 20px 20px 20px 20px;
		}

		/* Styles the lightbox, removes it from sight and adds the fade-in transition */

		.lightbox-target {
		position: fixed;
		top: -100%;
		width: 100%;
		background: rgba(0,0,0,.7);
		width: 100%;
		opacity: 0;
		-webkit-transition: opacity .5s ease-in-out;
		-moz-transition: opacity .5s ease-in-out;
		-o-transition: opacity .5s ease-in-out;
		transition: opacity .5s ease-in-out;
		overflow: hidden;
		 
		}

		/* Styles the lightbox image, centers it vertically and horizontally, adds the zoom-in transition and makes it responsive using a combination of margin and absolute positioning */

		.lightbox-target img {
		margin: auto;
		position: absolute;
		top: 0;
		left:0;
		right:0;
		bottom: 0;
		max-height: 0%;
		max-width: 0%;
		border: 3px solid white;
		box-shadow: 0px 0px 8px rgba(0,0,0,.3);
		box-sizing: border-box;
		-webkit-transition: .5s ease-in-out;
		-moz-transition: .5s ease-in-out;
		-o-transition: .5s ease-in-out;
		transition: .5s ease-in-out;
		  
		}

		/* Styles the close link, adds the slide down transition */

		a.lightbox-close {
		display: block;
		width:50px;
		height:95px;
		box-sizing: border-box;
		background: white;
		color: black;
		text-decoration: none;
		position: absolute;
		top: -80px;
		right: 0;
		-webkit-transition: .5s ease-in-out;
		-moz-transition: .5s ease-in-out;
		-o-transition: .5s ease-in-out;
		transition: .5s ease-in-out;
		}

		/* Provides part of the "X" to eliminate an image from the close link */

		a.lightbox-close:before {
		content: "";
		display: block;
		height: 30px;
		width: 1px;
		background: black;
		position: absolute;
		left: 26px;
		top:60px;
		-webkit-transform:rotate(45deg);
		-moz-transform:rotate(45deg);
		-o-transform:rotate(45deg);
		transform:rotate(45deg);
		}

		/* Provides part of the "X" to eliminate an image from the close link */

		a.lightbox-close:after {
		content: "";
		display: block;
		height: 30px;
		width: 1px;
		background: black;
		position: absolute;
		left: 26px;
		top:60px;
		-webkit-transform:rotate(-45deg);
		-moz-transform:rotate(-45deg);
		-o-transform:rotate(-45deg);
		transform:rotate(-45deg);
		}

		/* Uses the :target pseudo-class to perform the animations upon clicking the .lightbox-target anchor */

		.lightbox-target:target {
		opacity: 1;
		top: 0;
		bottom: 0;
		  overflow:scroll;
		}

		.lightbox-target:target img {
		max-height: 90%;
		max-width: 90%;
		}

		.lightbox-target:target a.lightbox-close {
		top: 0;
		}
	</style>
	
	<body>
		
		<?php if(!isset($_SESSION["iduser"])){ ?>
			<nav class="navbar navbar-expand-sm bg-dark navbar-dark fixed-top">
				<ul class="navbar-nav">
					<li class="nav-item">
						<a class="navbar-brand" href="#">Watchbot</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="#">Home</a>
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

			<div class="row" style="display:flex;align-items:center;height:100vh;">
				<div class="col-md-4">
					<img class="mx-auto d-block" src="images/01.png" width="60%">  
				</div>
				<div class="col-md-7" style="height:50vh;">
					<h1 class="display-3 text-white mb-4 text-left">WatchBot, an easy way to view your health data.</h1>
					<h5 class="text-white text-left">Buy our new watch and enjoy your personal bot. No need to spend hours creating your own dashboard to consult your health data, you just have to ask your bot what you want to consult and it will immediately give you the result.</h5>
					<br><br><br>
					<div class="card welcomecard">
						<div class="card-body">
							<h4 class="card-title text-white text-left">Start now !</h4>
							<p class="card-text text-white text-left">Get your new WatchBot Serie 1 and meet your personnal bot.</p>
							<button type="button" class="btn btn-primary float-left">Buy now</button>
						</div>
					</div>
					
				</div>
			</div>
		<?php } ?>
		
		<?php if(isset($_SESSION["iduser"])){ ?>
		
			<nav class="navbar navbar-expand-sm bg-dark navbar-dark fixed-top">
				<ul class="navbar-nav">
					<li class="nav-item">
						<a class="navbar-brand" href="#">Watchbot</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="#">Home</a>
					</li>
				</ul>
				<div class="navbar-collapse collapse w-100 order-3 dual-collapse2">
					<ul class="navbar-nav ml-auto">
						<li class="nav-item">
							<?php if($_SESSION["gender"] == "male"){ ?>
								<img src="images/avatar.png" class="rounded-circle user_img_msg mr-3" style="height:35px; width:35px;">
							<?php } ?>
							<?php if($_SESSION["gender"] == "female") { ?>
								<img src="images/female.png" class="rounded-circle user_img_msg mr-3" style="height:35px; width:35px;">
							<?php } ?>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="includes/logout.php"><i class="fas fa-sign-out-alt mr-2"></i></a>
						</li>
					</ul>
				</div>
			</nav>
			
			<div class="container-fluid h-100">
				<div class="row justify-content-center h-100">
					<div class="chat">
						<div class="card chatcard">
							<div class="card-header msg_head">
								<div class="d-flex bd-highlight">
									<div class="img_cont">
										<img src="images/bot.png" class="rounded-circle user_img">
										<span class="online_icon"></span>
									</div>
									<div class="user_info">
										<span>Chat with Bot</span>
										<p id="nbmessages" class="text-left">0 Messages</p>
									</div>
								</div>
								<span id="action_menu_btn"><i class="fas fa-ellipsis-v"></i></span>
								<div class="action_menu">
									<ul>
										<li id="clearmessages"><i class="fas fa-ban"></i> Clear messages</li>
									</ul>
								</div>
							</div>
							<div id="msgbody" class="card-body msg_card_body">
							</div>
							<div class="card-footer">
								<form id="chatbot" enctype="multipart/form-data" method="post" action="python/WebtoBot.py" autocomplete="off">
									<div class="input-group">
										<div class="input-group-append">
											<span class="input-group-text attach_btn"><i class=""></i></span>
										</div>
										<input id="iduser" type="hidden" name="iduser" class="invisible" value="<?php echo $_SESSION['iduser'];?>">
										<input id="gender" type="hidden" name="gender" class="invisible" value="<?php echo $_SESSION['gender'];?>">
										<textarea id="text" name="text" class="form-control type_msg remove-sharp" placeholder="Type your message..." required></textarea>
										<div class="input-group-append">
											<button type="submit" form="chatbot" class="btn input-group-text send_btn"><i class="fas fa-location-arrow"></i></button>
										</div>
									</div>
								</form>
							</div>
						</div>
					</div>
				</div>
			</div>
			
			<div id="imgfullscreen"></div>
		
		<?php } ?>


	</body>
	
	<script>
		$(document).ready(function(){
			$('#action_menu_btn').click(function(){
				$('.action_menu').toggle();
			});
		});
		
		$("#imgfullscreen").click(function() {
		  location.href = "../watchbot";
		});
			
		//DELETE MESSAGES
		$('#clearmessages').on('click',function() {         
			window.location.href = "includes/deleteallmessages.php";
		});
		
		//DISPLAY MESSAGES
		function displaymessage(id, avatar, iduser, text, img, status, date, nbmessages){
			if(text.length <= 7){
				date = date.substring(0, 5)
			}
			if(status == "human"){
				$(msgbody).append(`
					<div class="d-flex justify-content-end mb-4">
						<div class="msg_cotainer_send">${text}<span class="msg_time_send">${date}</span></div>
						<div class="img_cont_msg"><img src="${avatar}" class="rounded-circle user_img_msg"></div>
					</div>
				`);
			}
			else{
				if(img){
					$(msgbody).append(`
						<div class="d-flex justify-content-start mb-4">
							<div class="img_cont_msg">
								<img src="${avatar}" class="rounded-circle user_img_msg">
							</div>
							<div class="msg_cotainer">
								<a class="lightbox" href="#${img}">
								   <img src="${img}">
								</a>
								<span class="msg_time">${date}</span>
							</div>
						</div>
					`);
					
					$(imgfullscreen).append(`
						<div class="lightbox-target" id="${img}">
							<img src="${img}">
							<a class="lightbox-close" href="#"></a>
						</div>
					`);
				}
				else{
					$(msgbody).append(`
						<div class="d-flex justify-content-start mb-4">
							<div class="img_cont_msg">
								<img src="${avatar}" class="rounded-circle user_img_msg">
							</div>
							<div class="msg_cotainer text-left">${text}<span class="msg_time">${date}</span></div>
						</div>
					`);
				}
			}
			
			document.getElementById("nbmessages").innerHTML = nbmessages+" Messages";
		}
	</script>
	
	<?php
		$sql = "SELECT * FROM chat WHERE iduser=? ORDER BY date ASC;";
		$stmt = mysqli_stmt_init($conn);
		if(!mysqli_stmt_prepare($stmt, $sql)){
			echo "SQL : Get playlist failed";
		}
		else {
			mysqli_stmt_bind_param($stmt, "i", $_SESSION["iduser"]);
			mysqli_stmt_execute($stmt);
			$result = mysqli_stmt_get_result($stmt);
			$num_rows = mysqli_num_rows($result);

			while($row = mysqli_fetch_assoc($result)){
				$id = $row['id'];
				$avatar = $row['avatar'];
				$iduser = $row['iduser'];
				$text = $row['text'];
				$img = $row['img'];
				$status = $row['status'];
				$date = $row['date'];
				$nbmessages = $num_rows;
				echo "<script>displaymessage('$id', '$avatar', '$iduser', '$text', '$img', '$status', '$date', '$nbmessages');</script>";
			}
		}
	?>
		
</html>

