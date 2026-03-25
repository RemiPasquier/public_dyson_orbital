import sys
import numpy as np

def read_cube(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    comment1 = lines[0]
    comment2 = lines[1]

    header = lines[2:6]

    natoms = int(header[0].split()[0])
    origin = np.array(header[0].split()[1:], float)

    nx, *vx = header[1].split()
    ny, *vy = header[2].split()
    nz, *vz = header[3].split()

    nx = int(nx)
    ny = int(ny)
    nz = int(nz)

    vx = np.array(vx, float)
    vy = np.array(vy, float)
    vz = np.array(vz, float)

    atom_lines = lines[6:6 + natoms]

    data_lines = lines[6 + natoms:]
    data = np.array([float(x) for line in data_lines for x in line.split()])

    data = data.reshape((nx, ny, nz))

    return comment1, comment2, natoms, origin, nx, ny, nz, vx, vy, vz, atom_lines, data


def write_cube(filename, c1, c2, natoms, origin, nx, ny, nz, vx, vy, vz, atom_lines, data):
    with open(filename, 'w') as f:
        f.write(c1)
        f.write(c2)
        f.write(f"{natoms:5d} {origin[0]:12.6f} {origin[1]:12.6f} {origin[2]:12.6f}\n")
        f.write(f"{nx:5d} {vx[0]:12.6f} {vx[1]:12.6f} {vx[2]:12.6f}\n")
        f.write(f"{ny:5d} {vy[0]:12.6f} {vy[1]:12.6f} {vy[2]:12.6f}\n")
        f.write(f"{nz:5d} {vz[0]:12.6f} {vz[1]:12.6f} {vz[2]:12.6f}\n")

        for line in atom_lines:
            f.write(line)

        flat = data.flatten()
        for i in range(0, len(flat), 6):
            f.write(" ".join(f"{x:13.5e}" for x in flat[i:i+6]) + "\n")


def stride_cube(data, sx, sy, sz):
    return data[::sx, ::sy, ::sz]


def main():
    if len(sys.argv) != 6:
        print("Usage: python stride_cube.py input.cube output.cube sx sy sz")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    sx, sy, sz = map(int, sys.argv[3:])

    c1, c2, natoms, origin, nx, ny, nz, vx, vy, vz, atom_lines, data = read_cube(input_file)

    data_s = stride_cube(data, sx, sy, sz)

    nx_s, ny_s, nz_s = data_s.shape
    vx_s = vx * sx
    vy_s = vy * sy
    vz_s = vz * sz

    write_cube(output_file, c1, c2, natoms, origin,
               nx_s, ny_s, nz_s, vx_s, vy_s, vz_s, atom_lines, data_s)


if __name__ == "__main__":
    main()

