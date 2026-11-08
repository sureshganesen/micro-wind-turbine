// ==============================================================================
// Sustainable Micro Wind Turbine Harvester - Complete Mechanical Assembly
// Part Number: SG-WIND-006 | Drawing: DWG-WIND-006-REV-A
// Author: Suresh Ganesen (Atom Forge Studio / Politeknik Malaysia)
// ==============================================================================

use <turbine_blade.scad>
use <hub_assembly.scad>

$fn = 40;

module generator_housing() {
    // 12V Permanent Magnet DC Dynamo Can
    color([0.2, 0.2, 0.25])
    difference() {
        cylinder(d = 42.0, h = 65.0, center = true);
        // Motor shaft
        translate([0, 0, 32.5])
        cylinder(d = 8.0, h = 25.0);
    }
}

module mast_assembly() {
    // Class D Reinforced PVC / Carbon Mast (1.2m representation)
    color([0.85, 0.85, 0.85])
    translate([0, 0, -250])
    cylinder(d = 32.0, h = 500, center = true);
}

module complete_turbine() {
    // Mast
    mast_assembly();
    
    // Generator
    translate([0, 0, 35])
    rotate([90, 0, 0])
    generator_housing();
    
    // Hub
    translate([0, -45, 35])
    rotate([90, 0, 0]) {
        color([0.9, 0.1, 0.15])
        tri_blade_hub();
        
        // 3x Blades
        for (angle = [0, 120, 240]) {
            rotate([0, 0, angle])
            translate([hub_outer_d * 0.38, 0, 0])
            rotate([0, 90, 0])
            color([0.95, 0.95, 0.98])
            aerofoil_blade();
        }
    }
}

complete_turbine();
