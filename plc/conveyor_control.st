(* Conveyor Belt Control — IEC 61131-3 Structured Text *)
(* Controls a conveyor with start/stop, speed, and jam detection *)

PROGRAM ConveyorControl
VAR
    btn_start       : BOOL;
    btn_stop        : BOOL;
    sensor_jam      : BOOL;
    sensor_speed    : REAL;   (* Hz from encoder *)
    motor_enable    : BOOL;
    motor_speed_sp  : REAL := 50.0;   (* % *)
    alarm_jam       : BOOL;
    timer_jam       : TON;
    state           : INT := 0;   (* 0=IDLE 1=RUN 2=FAULT *)
END_VAR

CASE state OF
    0:  (* IDLE *)
        motor_enable := FALSE;
        IF btn_start AND NOT alarm_jam THEN
            state := 1;
        END_IF;

    1:  (* RUNNING *)
        motor_enable := TRUE;
        timer_jam(IN := sensor_jam, PT := T#3S);
        IF timer_jam.Q THEN
            alarm_jam := TRUE;
            state     := 2;
        END_IF;
        IF btn_stop THEN
            state := 0;
        END_IF;

    2:  (* FAULT *)
        motor_enable := FALSE;
        IF NOT sensor_jam THEN
            alarm_jam := FALSE;
            state     := 0;
        END_IF;
END_CASE;
END_PROGRAM
