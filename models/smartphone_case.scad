baseModelFilePath="/meshes/Samsung S20 Cover v7.stl";
font="Marsh Stencil";
decal_text="hello";

difference() {
    import(baseModelFilePath);
    translate([100,50,-1]) linear_extrude(height=10) text(decal_text,font=font);
}
