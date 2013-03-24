var isIE = (document.all) ? true : false;

var $ = function (id) {
	return "string" == typeof id ? document.getElementById(id) : id;
};

var Class = {
	create: function() {
		return function() { this.initialize.apply(this, arguments); }
	}
}

var Extend = function(destination, source) {
	for (var property in source) {
		destination[property] = source[property];
	}
}

var Bind = function(object, fun) {
	return function() {
		return fun.apply(object, arguments);
	}
}

var BindAsEventListener = function(object, fun) {
	return function(event) {
		return fun.call(object, (event || window.event));
	}
}

var CurrentStyle = function(element){
	return element.currentStyle || document.defaultView.getComputedStyle(element, null);
}

function addEventHandler(oTarget, sEventType, fnHandler) {
	if (oTarget.addEventListener) {
		oTarget.addEventListener(sEventType, fnHandler, false);
	} else if (oTarget.attachEvent) {
		oTarget.attachEvent("on" + sEventType, fnHandler);
	} else {
		oTarget["on" + sEventType] = fnHandler;
	}
};

function removeEventHandler(oTarget, sEventType, fnHandler) {
    if (oTarget.removeEventListener) {
        oTarget.removeEventListener(sEventType, fnHandler, false);
    } else if (oTarget.detachEvent) {
        oTarget.detachEvent("on" + sEventType, fnHandler);
    } else { 
        oTarget["on" + sEventType] = null;
    }
};

// Drag Program
var Drag = Class.create();
Drag.prototype = {
  // Target
  initialize: function(drag, options) {
	this.Drag = $(drag); // dragged target
	this._x = this._y = 0; // get the relative position of target
	this._marginLeft = this._marginTop = 0; // get margin
	// event target(for the use of remove event)
	this._fM = BindAsEventListener(this, this.Move);
	this._fS = Bind(this, this.Stop);
	
	this.SetOptions(options);
	
	this.Limit = !!this.options.Limit;
	this.mxLeft = parseInt(this.options.mxLeft);
	this.mxRight = parseInt(this.options.mxRight);
	this.mxTop = parseInt(this.options.mxTop);
	this.mxBottom = parseInt(this.options.mxBottom);
	
	this.LockX = !!this.options.LockX;
	this.LockY = !!this.options.LockY;
	this.Lock = !!this.options.Lock;
	
	this.onStart = this.options.onStart;
	this.onMove = this.options.onMove;
	this.onStop = this.options.onStop;
	
	this._Handle = $(this.options.Handle) || this.Drag;
	this._mxContainer = $(this.options.mxContainer) || null;
	
	this.Drag.style.position = "absolute";
	// Transparent
	if(isIE && !!this.options.Transparent){
		// Fill dragged target ******************************************************************************************
		with(this._Handle.appendChild(document.createElement("div")).style){
			width = height = "100%"; backgroundColor = "#fff"; filter = "alpha(opacity:0)"; fontSize = 0;
		}
	}
	// revise range
	this.Repair();
	addEventHandler(this._Handle, "mousedown", BindAsEventListener(this, this.Start));
  },
  // Set Prototype
  SetOptions: function(options) {
	this.options = {
		Handle:			"",
		Limit:			false,
		mxLeft:			0,
		mxRight:		9999,
		mxTop:			0,
		mxBottom:		9999,
		mxContainer:	"",
		LockX:			false,
		LockY:			false,
		Lock:			false,
		Transparent:	false,
		onStart:		function(){},
		onMove:			function(){},
		onStop:			function(){}
	};
	Extend(this.options, options || {});
  },
  // Drag Initial
  Start: function(oEvent) {
	if(this.Lock){ return; }
	this.Repair();
	// get the relative position of target
	this._x = oEvent.clientX - this.Drag.offsetLeft;
	this._y = oEvent.clientY - this.Drag.offsetTop;
	// get margin
	this._marginLeft = parseInt(CurrentStyle(this.Drag).marginLeft) || 0;
	this._marginTop = parseInt(CurrentStyle(this.Drag).marginTop) || 0;
	// mousemove: move ;  mouseup: stop
	addEventHandler(document, "mousemove", this._fM);
	addEventHandler(document, "mouseup", this._fS);
	if(isIE){
		// Lose Capture
		addEventHandler(this._Handle, "losecapture", this._fS);
		// Set mouse Capture
		this._Handle.setCapture();
	}else{
		// Windows.blur
		addEventHandler(window, "blur", this._fS);
		// Stop Prototype event
		oEvent.preventDefault();
	};
	// append event
	this.onStart();
  },
  // Revise Range
  Repair: function() {
	if(this.Limit){
		// revise error range parameter
		this.mxRight = Math.max(this.mxRight, this.mxLeft + this.Drag.offsetWidth);
		this.mxBottom = Math.max(this.mxBottom, this.mxTop + this.Drag.offsetHeight);
		// if container exist, set "position: relative || absolute" to set it's position before getting "offset"
		!this._mxContainer || CurrentStyle(this._mxContainer).position == "relative" || CurrentStyle(this._mxContainer).position == "absolute" || (this._mxContainer.style.position = "relative");
	}
  },
  // Drag
  Move: function(oEvent) {
	// Check if it's locked
	if(this.Lock){ this.Stop(); return; };
	// clear UserChoice
	window.getSelection ? window.getSelection().removeAllRanges() : document.selection.empty();
	// set moving parameter
	var iLeft = oEvent.clientX - this._x, iTop = oEvent.clientY - this._y;
	//set Range Limit
	if(this.Limit){
		// set range parameter
		var mxLeft = this.mxLeft, mxRight = this.mxRight, mxTop = this.mxTop, mxBottom = this.mxBottom;
		// if a container is planned, revise range parameter
		if(!!this._mxContainer){
			mxLeft = Math.max(mxLeft, 0);
			mxTop = Math.max(mxTop, 0);
			mxRight = Math.min(mxRight, this._mxContainer.clientWidth);
			mxBottom = Math.min(mxBottom, this._mxContainer.clientHeight);
		};
		// revise moving parameter
		iLeft = Math.max(Math.min(iLeft, mxRight - this.Drag.offsetWidth), mxLeft);
		iTop = Math.max(Math.min(iTop, mxBottom - this.Drag.offsetHeight), mxTop);
	}
	// position set, revise margin
	if(!this.LockX){ this.Drag.style.left = iLeft - this._marginLeft + "px"; }
	if(!this.LockY){ this.Drag.style.top = iTop - this._marginTop + "px"; }
	// append event
	this.onMove();
  },
  // Stop dragging
  Stop: function() {
	// remove event
	removeEventHandler(document, "mousemove", this._fM);
	removeEventHandler(document, "mouseup", this._fS);
	if(isIE){
		removeEventHandler(this._Handle, "losecapture", this._fS);
		this._Handle.releaseCapture();
	}else{
		removeEventHandler(window, "blur", this._fS);
	};
	// append event
	this.onStop();
  }
};