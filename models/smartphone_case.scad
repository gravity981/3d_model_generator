baseModelFilePath="/meshes/case_samsung_S20_tpu v8.3mf";
font="Marsh Stencil";
decal_text="hello world";
horizontal_offset=95;
vertical_offset=35;
font_size=10;
difference() {
    import(baseModelFilePath, convexity=3);
    translate([horizontal_offset,vertical_offset,-1]) linear_extrude(height=10)
    mirror([1,0,0]) 
    text(decal_text, font=font, size=font_size, valign="center", halign="center");
}
