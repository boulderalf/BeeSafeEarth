@YES: #0f0;
@NO: #cc2121;
@MAYBE: #ff0;
@NOT_REACHED: #ff0;

#blocks {
  line-color:#f45;
  line-width:2;
  polygon-opacity:.2;
  polygon-fill:#ae8;
}


#beesafeneighborhood {
  line-color:#594;
  line-width:0.5;
  polygon-opacity:0.5;
  polygon-fill:#ae8;
}


#parcels {
  line-color:gray;
  line-width:0.5;
}

#parcels[PLEDGE='YES'] {
  [zoom >= 15] {
    polygon-opacity:0.8;
    polygon-fill:@YES;
  }  
  [zoom < 15] {
    line-width:10;
    line-join:round;
    line-cap:round;
    line-color:@YES;
    polygon-opacity:0.8;
    polygon-fill:@YES;
  }
}

#parcels[PLEDGE='NO'] {
  [zoom >= 15] {
    polygon-opacity:0.8;
    polygon-fill:@NO;
  }  
  [zoom < 15] {
    line-width:10;
    line-join:round;
    line-cap:round;
    line-color:@NO;
    polygon-opacity:0.8;
    polygon-fill:@NO;
  }
}

#parcels[PLEDGE='MAYBE'] {
  [zoom >= 15] {
    polygon-opacity:0.8;
    polygon-fill:@MAYBE;
  }  
  [zoom < 15] {
    line-width:10;
    line-join:round;
    line-cap:round;
    line-color:@MAYBE;
    polygon-opacity:0.8;
    polygon-fill:@MAYBE;
  }
}

#addresses[ADDR_FMT="EXACT"] {
  text-name:"[ADDR_NUM]";
  text-face-name:"Arial Bold";
  text-size:9;
}

.streets {
    line-color:spin(darken(gray,36),-10);
    line-cap:round;
  	line-join:round;
	text-name:"[ROUTENAME]";
  	text-placement:line;
  	text-face-name: "Arial Bold"; 
}
