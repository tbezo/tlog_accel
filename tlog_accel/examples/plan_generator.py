from pylinac.plan_generator.dicom import PlanGenerator

# Use exported basic plan from Eclipse.
# Documentation: https://pylinac.readthedocs.io/en/latest/plan_generator.html#prerequisites
rt_plan_file = r"c:\temp\baseplan.dcm" # expoted basic plan from eclipse
generator = PlanGenerator.from_rt_plan_file(rt_plan_file,
                                            plan_name="MLC_accel25",
                                            plan_label="MLC_accel25")

generator.add_mlc_speed_beams(
    speeds=(25, 25, 25, 25, 25),
    roi_size_mm=28,
    y1=-190,
    y2=190,
    mu=100,
    default_dose_rate=600
)

generator.to_file(r"c:\temp\mlcspeed25.dcm")
