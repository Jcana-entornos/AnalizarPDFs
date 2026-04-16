<?php
if (isset($_FILES['pdf'])) {
    $archivo = escapeshellarg($_FILES['pdf']['tmp_name']);

    $python = "python3";
    $script = "contadorespecialidades.py";

    $comando = "$python $script $archivo 2>&1";
    $resultado = shell_exec($comando);
    $datos = json_decode($resultado, true);
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Resultado PDF</title>

    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f4fdf6;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            background: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0, 128, 0, 0.15);
            text-align: center;
            width: 360px;
        }

        h2 {
            color: #1b5e20;
            margin-bottom: 15px;
        }

        .result {
            font-size: 18px;
            color: #2e7d32;
            margin: 20px 0;
            font-weight: bold;
        }

        .btn {
            display: inline-block;
            background: #2e7d32;
            color: white;
            text-decoration: none;
            padding: 12px 18px;
            border-radius: 8px;
            transition: 0.3s;
            font-size: 16px;
        }

        .btn:hover {
            background: #1b5e20;
        }
        .btn {
            display: inline-block;
            margin-top: 20px; /* 👈 separa del resultado */
        }
    </style>
</head>

<body>

<div class="container">
    <h2>Resultado del análisis</h2>

    <div class="result">
        <?php
        if ($datos) {
            foreach ($datos as $esp => $info) {
                echo "<p><strong>$esp</strong><br>";
                echo "Total: " . $info['total'] . "<br>";
                echo "Admitidos: " . $info['admitidos'] . "</p>";
            }
        } else {
            echo "Error procesando el archivo.";
        }
        ?>
    </div>

    <a class="btn" href="Formulario.html">Volver</a>
</div>

</body>
</html>