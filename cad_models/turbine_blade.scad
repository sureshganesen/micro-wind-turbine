// ==============================================================================
// Sustainable Micro Wind Turbine Harvester - Cambered Aerofoil Blade
// Part Number: SG-WND-BLD1 | Drawing: DWG-WIND-006-REV-A
// Author: Suresh Ganesen (Atom Forge Studio / Politeknik Malaysia)
// Standard: ISO Standard / ASME Y14.5M (Tolerance +/- 0.20 mm)
// Material: High-Modulus UV-Stabilized PETG / ASA
// ==============================================================================

$fn = 60;

// Blade Specifications
blade_length = 195.0;      // Rotor radius 210mm - 15mm hub offset
chord_root   = 52.0;       // Root chord width (mm)
chord_tip    = 28.0;       // Tip chord width (mm)
camber_max   = 14.5;       // Optimal aerodynamic lift camber (mm)
thickness    = 3.2;        // Blade wall thickness
root_twist   = 18.0;       // Aerodynamic pitch angle at root (deg)
tip_twist    = 4.5;        // Aerodynamic pitch angle at tip (deg)
mount_hole_d = 4.2;        // M4 mounting screw clearance
mount_spacing= 16.0;

module aerofoil_slice(chord, camber, thick) {
    // Cambered thin aerofoil cross-section (approx NACA 4-digit camber curve)
    difference() {
        hull() {
            // Leading edge radius
            translate([0, 0, 0]) circle(r = thick * 0.8);
            // Upper camber peak
            translate([chord * 0.35, camber * 0.45, 0]) circle(r = thick * 0.6);
            // Trailing edge
            translate([chord, 0, 0]) circle(r = 0.4);
        }
        // Hollow interior for lightweight aerodynamic shell
        offset(r = -thick * 0.6) {
            hull() {
                translate([0, 0, 0]) circle(r = thick * 0.8);
                translate([chord * 0.35, camber * 0.45, 0]) circle(r = thick * 0.6);
                translate([chord, 0, 0]) circle(r = 0.4);
            }
        }
    }
}

module aerofoil_blade() {
    union() {
        // Root mounting flange
        difference() {
            cube([32, 22, 10], center = true);
            // M4 fastener holes
            translate([0, -mount_spacing/2, 0]) cylinder(d = mount_hole_d, h = 20, center = true);
            translate([0,  mount_spacing/2, 0]) cylinder(d = mount_hole_d, h = 20, center = true);
        }
        
        // Aerodynamic lofted blade span
        translate([0, 0, 5])
        linear_extrude(height = blade_length, twist = -(root_twist - tip_twist), scale = chord_tip / chord_root, slices = 50) {
            rotate([0, 0, root_twist])
            translate([-chord_root * 0.25, 0, 0])
            aerofoil_slice(chord_root, camber_max, thickness);
        }
        
        // Aerodynamic rounded tip cap
        translate([0, 0, blade_length + 5])
        sphere(r = 3.5);
    }
}

aerofoil_blade();
