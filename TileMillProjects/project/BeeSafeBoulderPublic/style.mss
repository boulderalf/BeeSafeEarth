@YES: #0f0;
@NO: #cc2121;
@MAYBE: #ff0;
@NOT_REACHED: #ff0;
@MARKER_WIDTH: 20;


.address[PLEDGE='YES'][SHOW_ON_MA='1'] {
  marker-file:url("./bee.png");
  marker-allow-overlap:true;
  marker-opacity: 1.0;
  marker-width:@MARKER_WIDTH;
  [zoom<=11] { marker-allow-overlap:false; }
/*
  [zoom=14] { marker-width:@MARKER_WIDTH * 2; }
  [zoom=15] { marker-width:@MARKER_WIDTH * 4; }
  [zoom=16] { marker-width:@MARKER_WIDTH * 8; }
  [zoom=17] { marker-width:@MARKER_WIDTH * 16; }
  [zoom=18] { marker-width:@MARKER_WIDTH * 32; }
  [zoom=19] { marker-width:@MARKER_WIDTH * 64; }
  [zoom=20] { marker-width:@MARKER_WIDTH *128; }
  [zoom=21] { marker-width:@MARKER_WIDTH *256; }
  [zoom=22] { marker-width:@MARKER_WIDTH *512; }
   */
}

/*
.address {
  marker-fill:#000;
  marker-opacity:1.0
  }
*/

#streets {
  line-width:1;
  line-color:lightgray;
}


#neighborhood {
  line-color:#594;
  line-width:0.5;
  polygon-opacity:0.5;
  polygon-fill:#ae8;
}
