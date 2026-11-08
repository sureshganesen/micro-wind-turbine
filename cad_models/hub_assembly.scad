// ==============================================================================
// Sustainable Micro Wind Turbine Harvester - 120° Tri-Blade Hub Mount
// Part Number: SG-WND-HUB1 | Drawing: DWG-WIND-006-REV-A
// Author: Suresh Ganesen (Atom Forge Studio / Politeknik Malaysia)
// Standard: ISO Standard / ASME Y14.5M (Shaft Bore ⌀8.00 H7)
// ==============================================================================

$fn = 80;

hub_outer_d  = 72.0;       // Hub outer diameter
hub_height   = 28.0;       // Hub thickness
shaft_bore_d = 8.00;       // ⌀8.00 H7 (+0.015/-0.000 mm) dynamo shaft
set_screw_d  = 3.3;        // M4 grub/set screw tap hole (3.3 mm for M4x0.7)
blade_slot_w = 22.4;       // Blade root slot width
blade_slot_d = 10.2;       // Blade root slot depth
mount_pitch  = 16.0;

module tri_blade_hub() {
    difference() {
        // Main aerodynamically tapered nose hub
        union() {
            cylinder(d1 = hub_outer_d, d2 = hub_outer_d * 0.85, h = hub_height, center = true);
            // Nose cone dome
            translate([0, 0, hub_height/2])
            sphere(d = hub_outer_d * 0.85);
        }
        
        // Central dynamo motor shaft bore (ISO H7 tolerance)
        cylinder(d = shaft_bore_d, h = hub_height * 3, center = true);
        
        // Dual M4 set screw clamping holes (90 deg offset)
        translate([0, 0, 0])
        rotate([90, 0, 0])
        cylinder(d = set_screw_d, h = hub_outer_d, center = true);
        
        // 3x Blade mounting slots radially spaced at exactly 120.0 deg +/- 0.2 deg
        for (a = [0, 120, 240]) {
            rotate([0, 0, a]) {
                // Blade root insertion pocket
                translate([hub_outer_d * 0.38, 0, -hub_height * 0.1])
                cube([30, blade_slot_w, blade_slot_d + 2], center = true);
                
                // M4 through-bolt clamping holes
                translate([hub_outer_d * 0.38, -mount_pitch/2, 0])
                cylinder(d = 4.2, h = hub_height * 1.5, center = true);
                
                translate([hub_outer_d * 0.38,  mount_pitch/2, 0])
                cylinder(d = 4.2, h = hub_height * 1.5, center = true);
            }
        }
    }
}

tri_blade_hub();
