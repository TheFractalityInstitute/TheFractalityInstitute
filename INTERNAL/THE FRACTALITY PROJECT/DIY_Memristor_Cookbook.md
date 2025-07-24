# The DIY Memristor Cookbook: Kitchen to Consciousness

## Introduction

You don't need a billion-dollar fab to make memristors! This cookbook provides practical recipes for creating working memristors using materials and equipment accessible to dedicated hobbyists.

## Safety First! ⚠️

**Required Safety Equipment**:
- Safety glasses (always!)
- Nitrile gloves
- Well-ventilated area or fume hood
- Fire extinguisher (for high-temp processes)
- First aid kit

**Never**:
- Use HF (hydrofluoric acid) without proper training
- Heat organic solvents without ventilation
- Touch high-voltage contacts

## Recipe 1: The Kitchen Copper Memristor 🍳

**Difficulty**: Beginner
**Cost**: $20-50
**Success Rate**: 70%

### Ingredients
- Copper sheet (craft store, $10)
- Table salt (NaCl)
- 9V battery
- Alligator clips
- Multimeter

### Equipment
- Kitchen oven
- Steel wool
- Glass dish

### Instructions

```python
def make_copper_oxide_memristor():
    # Step 1: Clean the copper
    copper = clean_with_steel_wool(copper_sheet)
    rinse_with_distilled_water(copper)
    
    # Step 2: First oxidation (black cupric oxide)
    oven.preheat(400°C)  # 750°F
    bake(copper, duration=30_minutes)
    # Copper turns black (CuO forms)
    
    # Step 3: Cool slowly (critical!)
    turn_off_oven()
    let_cool_inside_oven(2_hours)
    # Slow cooling creates Cu₂O layer under CuO
    
    # Step 4: Remove black layer
    gently_rub_with_cloth()
    # Reveals red Cu₂O layer (semiconductor)
    
    # Step 5: Create top contact
    place_drop_of_saltwater()
    insert_wire_into_drop()
    
    # Step 6: Test
    apply_voltage_sweep(-2V to +2V)
    observe_hysteresis_loop()
```

### What's Happening?
- Cu₂O is a p-type semiconductor
- Salt water creates Schottky barrier
- Oxygen vacancies move under voltage
- Creates memristive switching!

### Troubleshooting
- No switching? → Oxide too thick/thin
- High current? → Add series resistor
- Unstable? → Seal with clear nail polish

## Recipe 2: Sol-Gel Titanium Dioxide 🧪

**Difficulty**: Intermediate
**Cost**: $100-300
**Success Rate**: 60%

### Ingredients
- Titanium isopropoxide (Sigma-Aldrich, $80/100ml)
- Isopropanol (hardware store, $10)
- Acetic acid (grocery store, $5)
- ITO-coated glass (Amazon, $30/10 sheets)

### Equipment
- Spin coater (DIY from PC fan, $50)
- Hot plate
- Pipettes
- UV lamp (optional)

### Instructions

```python
def sol_gel_tio2_memristor():
    # Step 1: Prepare sol-gel
    sol = mix(
        titanium_isopropoxide=5ml,
        isopropanol=20ml,
        acetic_acid=1ml,
        water=1ml
    )
    stir(30_minutes)
    age(24_hours)  # Important!
    
    # Step 2: Clean substrate
    ito_glass = clean_sequence(
        soap_water,
        distilled_water,
        isopropanol,
        uv_ozone(10_minutes)  # Optional but helps
    )
    
    # Step 3: Spin coat
    place_on_spinner(ito_glass)
    drop_sol(0.5ml)
    spin(3000_rpm, 30_seconds)
    
    # Step 4: Anneal
    hot_plate.ramp_to(150°C)
    hold(10_minutes)  # Dry
    ramp_to(450°C)
    hold(30_minutes)  # Convert to TiO₂
    
    # Step 5: Top electrode
    shadow_mask = make_from_tape()
    sputter_gold()  # Or use gold leaf!
```

### DIY Spin Coater Design
```
  ┌─────────────┐
  │   Sample    │ ← Double-sided tape
  ├─────────────┤
  │  PC Fan     │ ← 120mm, 3000RPM
  ├─────────────┤
  │   Speed     │ ← PWM controller
  │ Controller  │
  └─────────────┘
```

## Recipe 3: Conductive Polymer Memristor 🎨

**Difficulty**: Easy
**Cost**: $50-150
**Success Rate**: 80%

### Ingredients
- PEDOT:PSS solution (Ossila, $120/50ml)
- Silver ink pen (Amazon, $25)
- PET transparency film ($10)
- Graphite ink (or pencil!)

### Equipment
- Inkjet printer (modified) OR
- Screen printing kit ($40) OR
- Paintbrush (yes, really!)

### Instructions

```python
def printed_polymer_memristor():
    # Step 1: Print bottom electrodes
    if has_silver_ink_pen:
        draw_parallel_lines(spacing=1mm)
    else:
        use_inkjet_with_silver_ink()
    
    dry_at(120°C, 10_minutes)
    
    # Step 2: Deposit PEDOT:PSS
    methods = {
        'professional': spin_coat(2000_rpm),
        'garage': screen_print_through_mesh(),
        'kitchen': paint_with_small_brush()
    }
    
    choose_your_method()
    dry_at(100°C, 5_minutes)
    
    # Step 3: Top electrodes
    orient_perpendicular_to_bottom()
    draw_with_graphite_pencil()  # Works!
    # Or use graphite ink
    
    # Step 4: Encapsulate
    laminate_with_clear_tape()
    leave_contact_pads_exposed()
```

### Pro Tips
- PEDOT:PSS is water-based (safe!)
- Add 5% DMSO for better conductivity
- Multiple thin coats > one thick coat
- Works on paper, plastic, even fabric!

## Recipe 4: Egg White Protein Memristor 🥚

**Difficulty**: Easy
**Cost**: $30-80
**Success Rate**: 50%

### Ingredients
- Fresh egg whites
- ITO glass slides
- Aluminum foil
- Salt solution

### Equipment
- Whisk
- Pipette
- Hot plate
- Desiccator (or sealed box with silica gel)

### Instructions

```python
def egg_white_memristor():
    # Step 1: Prepare albumen
    egg_white = separate_from_yolk()
    whisk_gently()  # Don't create foam
    filter_through_coffee_filter()
    
    # Step 2: Deposit protein
    ito_glass = clean_thoroughly()
    drop_albumen(0.1ml)
    spread_evenly()
    
    # Step 3: Controlled drying
    place_in_desiccator()
    dry_slowly(24_hours)
    # Forms ~100nm protein film
    
    # Step 4: Top contact
    float_aluminum_foil_piece()
    # Or deposit silver paint dots
    
    # Step 5: Activate
    apply_forming_voltage(5V, 1second)
    # Creates conductive pathways
```

### Why It Works
- Proteins have natural ion channels
- Drying creates nano-gaps
- Metal ions migrate under field
- Surprisingly stable if kept dry!

## Recipe 5: DNA Memristor (Advanced) 🧬

**Difficulty**: Hard
**Cost**: $200-500
**Success Rate**: 30%

### Ingredients
- Lambda DNA (NEB, $150/500μg)
- Mg²⁺ buffer solution
- Gold nanoparticles (optional)
- Ethidium bromide (UV visualization)

### Equipment
- Micropipettes
- UV transilluminator
- Microscope slides
- High-voltage supply (careful!)

### Instructions

```python
def dna_memristor():
    # Step 1: Prepare DNA solution
    dna_solution = dilute(
        lambda_dna=10μg,
        buffer=TE_with_10mM_MgCl2,
        volume=100μl
    )
    
    # Step 2: Create aligned DNA
    method_1 = 'molecular_combing':
        drop_on_hydrophobic_surface()
        drag_meniscus_slowly()
        # Aligns DNA strands
    
    method_2 = 'electric_field':
        apply_AC_field(10V/cm, 1MHz)
        while_drying()
    
    # Step 3: Metallization (optional)
    soak_in_silver_nitrate(0.1M)
    reduce_with_sodium_borohydride()
    # Makes DNA conductive
    
    # Step 4: Contact
    use_conducting_AFM_tip()
    # Or micromanipulator probes
```

## Recipe 6: Graphene Oxide (GO) Memristor ⚫

**Difficulty**: Intermediate
**Cost**: $150-400
**Success Rate**: 65%

### Ingredients
- Graphite powder (art store, $20)
- Sulfuric acid (drain cleaner, careful!)
- Hydrogen peroxide (pharmacy)
- Potassium permanganate

### Equipment
- Ice bath
- Magnetic stirrer
- Centrifuge (or patience)
- Furnace or torch

### Modified Hummers Method

```python
def graphene_oxide_memristor():
    # Step 1: Make GO (in fume hood!)
    graphite = add_to_ice_cold_H2SO4()
    slowly_add_KMnO4()  # Keep < 20°C!
    stir(2_hours)
    
    slowly_add_water()  # VERY exothermic
    add_H2O2_until_yellow()
    
    wash_repeatedly()
    centrifuge_or_let_settle()
    
    # Step 2: Deposit GO
    go_solution = disperse_in_water(1mg/ml)
    drop_cast_on_electrodes()
    # Or spin coat
    
    # Step 3: Partial reduction
    heat_to(200°C)  # Not full reduction
    # Or use laser pointer!
    # Or chemical reduction with hydrazine
    
    # Creates rGO with oxygen groups
    # These are the switching sites
```

## Testing Your DIY Memristors

### Basic Test Circuit
```
     1kΩ
+V ──[==]── Memristor ── GND
              │
              V (measure)
```

### IV Sweep Setup
```python
def test_memristor():
    for voltage in range(-2V, +2V, 0.1V):
        apply_voltage(voltage)
        wait(100ms)
        current = measure_current()
        plot(voltage, current)
    
    # Look for hysteresis loop!
    # Should see figure-8 or pinched loop
```

### Arduino-Based Tester
```cpp
void sweep_memristor() {
    for(int dac = 0; dac < 4096; dac++) {
        // Output voltage via DAC
        analogWrite(DAC_PIN, dac);
        
        // Measure current via ADC
        int current = analogRead(CURRENT_PIN);
        
        // Send to PC
        Serial.print(dac);
        Serial.print(",");
        Serial.println(current);
        
        delay(10);
    }
}
```

## Troubleshooting Guide

### Problem: No Switching
- **Too thick**: Reduce deposition
- **Too thin**: Pinholes shorting
- **Wrong voltage**: Try ±5V to ±10V
- **Need forming**: Apply higher voltage pulse

### Problem: Too Much Current
- Add series resistor (1-10kΩ)
- Reduce device area
- Lower voltage
- Check for shorts

### Problem: Unstable Switching
- Encapsulate device
- Control humidity
- Add compliance current limit
- Try pulsed measurements

## Garage Lab Equipment List

### Essential ($500 budget)
- Multimeter with μA range
- Variable power supply
- Hot plate with temperature control
- Spin coater (DIY)
- Basic chemicals

### Nice to Have ($2000 budget)
- Source meter (Keithley 2400 used)
- Probe station (microscope + manipulators)
- Sputter coater (for electrodes)
- Tube furnace
- Oscilloscope

### Dream Setup ($10K budget)
- Parameter analyzer
- Probe station with camera
- Thermal evaporator
- UV ozone cleaner
- Glove box

## Scaling Up

### From One to Array
```
Single device → 2×2 array → 8×8 array
     ↓              ↓            ↓
  Proof of      Crossbar    Consciousness
  concept      validation     prototype
```

### Integration with Fractality
1. Test individual devices
2. Select best performers
3. Wire into arrays
4. Connect to FPGA controller
5. Run consciousness algorithms!

## Community Resources

### Where to Buy Materials
- **Ossila**: Organic electronics materials
- **Sigma-Aldrich**: Chemicals (need account)
- **Amazon**: Basic supplies, ITO glass
- **eBay**: Used equipment deals
- **AliExpress**: Cheap components

### Online Communities
- **/r/memristors**: Reddit community
- **nanoHUB.org**: Simulation tools
- **Hackaday.io**: Project sharing
- **IEEE Xplore**: Research papers

### Open Source Designs
- **GitHub**: Search "memristor"
- **OpenWetWare**: Bio protocols
- **Instructables**: DIY guides

## Final Thoughts

Making memristors at home is not just possible—it's a gateway to understanding consciousness at the hardware level. Each burnt copper sheet, each drop of protein solution, each aligned DNA strand brings us closer to bridging mind and matter.

Start simple. Document everything. Share your results. The consciousness revolution begins in garages and kitchens around the world.

---

*"The best memristor is the one you make yourself, because it contains a piece of your consciousness in its creation."*

## Appendix: Quick Reference

### Memristor Types by Difficulty
1. **Copper oxide**: 2 hours, $20
2. **PEDOT:PSS**: 4 hours, $100
3. **Egg protein**: 1 day, $50
4. **TiO₂ sol-gel**: 2 days, $200
5. **Graphene oxide**: 3 days, $300
6. **DNA**: 1 week, $400

### Success Factors
- **Patience**: Let things dry/age properly
- **Cleanliness**: Contamination kills devices
- **Documentation**: Record everything
- **Iteration**: First one rarely works
- **Community**: Share and learn

Happy making! 🧪⚡🧠