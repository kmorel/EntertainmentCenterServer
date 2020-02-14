// JavaScript Document

function reloadPage() {
	$('#systemMenu').popup('close');
	location.reload(true);
}

function openServerManager() {
	$('#systemMenu').popup('close');
	window.open('http://' + window.location.hostname + ':9001', '_blank');
}

function restartServer() {
	$('#systemMenu').popup('close');
	window.open('http://' + window.location.hostname + ':9001/?processname=tvremote&action=restart', '_blank');
}

function getButtonSize() {
	var screenWidth = $(window).width();
	var screenHeight = $(window).height();

	// First guess, the display is 6 buttons across.
	var buttonSize = screenWidth/6;
	
	// Check to make sure the display is tall enough for this size. The height
	// must accomodate 4 buttons in the main area plus the power plus the mute
	// plus potentially tabs.
	if (screenHeight < buttonSize*7) {
		buttonSize = screenHeight/7;
	}

	return parseInt(buttonSize);
}

function initGUI() {
	var buttonSize = getButtonSize();
	var screenWidth = $(window).width();
	// Some padding to remove from widths to compensate for scroll bars,
	// which tend to be larger on larger displays.
	var widthFudge = 10;
	if (screenWidth > 700) {
		widthFudge = 40;
	}

	$('.PowerSelect').width(screenWidth - buttonSize - widthFudge - 10);

	$('#powerButton').width(buttonSize);
	$('#powerButton').height(buttonSize);

	$('.VolumeSelect').width(screenWidth - buttonSize - widthFudge);

	$('#mute').width(buttonSize);
	$('#mute').height(buttonSize);

	$('#systemMenuButton').width(buttonSize);
	$('#systemMenuButton').height(buttonSize);

	$('.ButtonPanel').width(6*buttonSize);
	$('.ButtonPanel').height(4*buttonSize);

	setInterval(refreshStatus, 900000);
}

function getStatus() {
	$('#systemMenu').popup('close');
	refreshStatus();
}

function refreshStatus() {
	$.getJSON('/status', showStatus);
}

function showStatus(data) {
	//$('#status').html('Refreshing Status');
	setUpModeByName(data.mode);
	if (!usingVolumeSlider) {
		//$('#volume').val(data.volume);
		$('#volume').val(0);
		$('#volume').slider('refresh');
	}
	setMuteFlag(data.mute);
}

function pushToPage(url) {
	$('#status').load(encodeURI(url))
	//new Image().src = url;
}

usingVolumeSlider = false;

function volumeSliderStart() {
	usingVolumeSlider = true;
}

function volumeSliderStop(newValue) {
	setVolume(newValue);
	usingVolumeSlider = false;
	$('#volume').val(0);
	$('#volume').slider('refresh');
}

function setVolume(newValue) {
	//pushToPage('/set-volume/' + newValue);
	if (newValue < 0) {
		pushToPage('/volume-down/' + -newValue)
	} else if (newValue > 0) {
		pushToPage('/volume-up/' + newValue)
	}
}

muteFlag = false;

function setMuteFlag(flag) {
	if (flag) {
		$('#mute').attr('src', '/static/icons/volume-mute.png');
	} else {
		$('#mute').attr('src', '/static/icons/volume-on.png');
	}
	muteFlag = flag;
}

function sendMuteFlag(flag) {
	setMuteFlag(flag)
	pushToPage("/set-mute/" + (flag ? 1 : 0));
}

function toggleMute() {
	sendMuteFlag(!muteFlag)
}

function getModeString() {
	return $('#state').val();
}

function setUpSelectedMode() {
	var modeName = getModeString();
	var modeId = modeName.replace(/\s/g, "");
	$('.ControlArea').each(function(index) {
		if (this.id == modeId) {
			this.style.display = '';
		} else {
			this.style.display = 'none';
		}
	});
	if (modeName == 'Everything Off') {
		$('#powerButton').attr('src', '/static/icons/power-off.png');
	} else {
		$('#powerButton').attr('src', '/static/icons/power-on.png');
	}
}

function setUpModeByName(modeName) {
	$('#state').val(modeName).attr('selected', true).siblings('option').removeAttr('selected');
	$('#state').selectmenu('refresh', true);
	setUpSelectedMode();
}

function sendMode() {
	setUpSelectedMode();
	pushToPage("/set-mode/" + getModeString());
}

function sendModeByName(modeName) {
	setUpModeByName(modeName);
	sendMode();
}

function send(device, command) {
	pushToPage("/send/" + device + "/" + command);
}

function sendBluRay(command) {
	pushToPage("/bluray/send/" + command);
}
